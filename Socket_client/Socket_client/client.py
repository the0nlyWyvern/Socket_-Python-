import socket

HEADER = 64 #bytes
PORT = 8888
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send_msg(msg):
    enc_msg = msg.encode('utf-8')
    send_length = str(len(enc_msg)).encode('utf-8')
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(enc_msg)
    print(client.recv(2048).decode('utf-8'))

def run_client():
    connecting = False
    while 1:
        SERVER_IP = input('''Input SERVER IP to continue: 
Or type "myip" to input your IP (In case you are running both on the same computer)
>''')
        if SERVER_IP == 'myip':
            SERVER_IP = socket.gethostbyname(socket.gethostname())

        try:
            client.connect((SERVER_IP, PORT))
            send_msg('')
            break
        except:
            print('\nCONNECTION FAILED')
    
    while 1:
        msg = input('>>')
        try:
            send_msg(msg)
            if msg == '-quit':
                print('CONNECTION REMOVED. THANK YOU FOR USING OUR PROGRAM')
                break
        except:
            print('SERVER WAS FORCED TO REMOVED YOUR CONNECTION.\nYou may close this program')
            break

run_client()
#192.168.23.1 
#example: look up: 2021-12-27 SJC, Lộc phát tài, WBTC, NEO