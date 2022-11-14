import socket
import threading
from requests import get
import json
from time import sleep
#import file .py
import UI as GUI

# we use the 2nd link
url_links = ['https://tygia.com/json.php?ran=0&rate=0&gold=1&bank=VIETCOM&date=now',
             'https://tygia.com/json.php', 'https://www.dongabank.com.vn/exchange/export']

HEADER = 64
PORT = 8888

SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDR)


def update_database():
    while True:
        print('~SERVER~ Updating database')
        with open('database/Ty_gia_vang.json', mode='w') as f:
            get_http = json.loads(
                get(url_links[1]).text.encode().decode('utf-8-sig'))
            f.write(json.dumps(get_http))
            f.close()
        print('~SERVER~ Database is up-to-date')
        sleep(1800)  # 1800 seconds = 30 minutes


def look_up(date: str, type: str):
    res = []
    with open('database/Ty_gia_vang.json', mode='r') as f:
        data = json.loads(f.read())
        f.close()
        for i in data['golds']:
            f = i['updated'].find(date)
            if f != -1:
                val = i['value']
                for j in val:
                    if j['type'] == type:
                        res.append(j)
    return res


def verify_account(username: str, password: str) -> bool:
    with open('database/account.txt', mode='r') as f:
        for row in f:
            s = safe_split(row, ',')
            if s:
                s[1] = s[1].replace('\n', '')
                if s[0] == username and s[1] == password:
                    return True
    return False


def register(username: str, password: str) -> bool:
    if not verify_account(username, password):
        with open('database/account.txt', mode='a') as f:
            f.write(username + ',' + password + '\n')
            return True
    return False


def get_msg(cont):
    msg_length = cont.recv(HEADER).decode('utf-8')
    if msg_length:
        msg = cont.recv(int(msg_length)).decode('utf-8')
        return msg
    else:
        return None


def send_msg(cont, text: str):
    cont.send(text.encode('utf-8'))


def print_msg_info(msg, user):
    print(f"User {user}: [{addr}] {msg}")


def safe_split(msg, char) -> list:
    msg = msg.split(char)
    if len(msg) == 2:
        return msg
    if len(msg) == 1:
        return []
    res = []
    res.append(msg[0])
    s = msg[1]
    for i in range(2, len(msg)):
        s += char + msg[i]
    res.append(s)
    return res


def remove_all_conts(cont, addr):
    command = input()
    if command == '-quit':
        print('~SERVER~ server has seen a command to close all connections.')
        send_msg(cont, 'SERVER IS REMOVING YOUR CONNECTION')
        cont.close()


def execution_a_client(cont, addr):
    '''Xử lí các tác vụ liên quan giữa server và client'''
    print(f'~SERVER~ DETECTING A NEW CONNECTION FROM: {addr} <<<')
    send_msg(cont, GUI.combine(GUI.welcome(
        SERVER_NAME=socket.gethostname(), SERVER_IP=SERVER), GUI.help()))

    username = ''
    MODE = 'waiting'
    while 1:
        try:
            msg = get_msg(cont)
        except:
            print(f'~SERVER~ Lost connection to client {addr}!!!')
            break

        if msg:
            if msg == '-quit':
                send_msg(cont, 'REMOVING CONNECTION')
                print(f'~{addr}~ has been removed.')
                break

            elif msg == '-help':
                send_msg(cont, GUI.help())

            elif msg == '-signin':
                print(f'~{addr}~ is signning in')
                send_msg(cont, GUI.log_in_instruction())
                MODE = 'signin'

            elif msg == '-signup':
                print(f'~{addr}~ is creating new account')
                send_msg(cont, GUI.log_in_instruction(False))
                MODE = 'signup'

            elif MODE == 'signin':
                msg = safe_split(msg, ' ')
                if msg:
                    if verify_account(msg[0], msg[1]):
                        username = msg[0]
                        print(
                            f'~{addr}~ Successfully access: {addr[0]} is "{username}"')
                        send_msg(cont, GUI.combine(
                            f'Log in successfully! WELCOME "{username}\n"', GUI.look_up_instruction()))
                        MODE = 'look_up'
                    else:
                        print(f'~{addr}~ Access failure')
                        send_msg(
                            cont, 'Username or Password may be wrong, type again:')
                else:
                    send_msg(cont, GUI.typo_error())

            elif MODE == 'signup':
                msg = safe_split(msg, ' ')
                if msg:
                    if register(msg[0], msg[1]):
                        username = msg[0]
                        print(
                            f'~{addr}~ Account created with name: "{username}"')
                        send_msg(cont, GUI.combine(f'A new account has been created. WELCOME "{username}"\n',
                                                   GUI.look_up_instruction()))
                        MODE = 'look_up'
                    else:
                        print(f'~{addr}~ Account is already exists')
                        send_msg(
                            cont, 'Account is already exists, you can type "-signin" to continue\nOr type again: ')
                else:
                    send_msg(cont, GUI.typo_error())

            elif MODE == 'look_up':
                msg = safe_split(msg, ' ')
                if msg:
                    print(f'~{addr}~ is looking up {msg}')
                    res = look_up(msg[0], msg[1])
                    print(f'~{addr}~ {len(res)} results found')
                    if len(res) > 0:
                        send_msg(cont, GUI.gold_info(res))
                    else:
                        send_msg(cont, 'Sorry, did not find any results')
                else:
                    send_msg(cont, GUI.typo_error())
            else:
                send_msg(
                    cont, 'I do not understand (may be you have not logged in)')

    cont.close()
    print(f'~SERVER~ CONNECTION FROM {addr} HAS BEEN REMOVED<<<')


def run_server():
    t1 = threading.Thread(target=update_database)
    t1.start()

    server.listen()
    print(f'Server is waiting for orders')
    while True:
        connect, address = server.accept()
        t2 = threading.Thread(target=execution_a_client,
                              args=(connect, address))
        t2.start()
        t3 = threading.Thread(target=remove_all_conts, args=(connect, address))
        t3.start()


print('SETUP COMPLETE - SERVER IS READY TO GO')
print(GUI.welcome(SERVER_NAME=socket.gethostname(), SERVER_IP=SERVER))
run_server()
