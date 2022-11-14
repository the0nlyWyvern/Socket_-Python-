def welcome(SERVER_NAME: str, SERVER_IP: str) -> str:
    return f'''
 _______________________________________________________
|                                                       |
|\t\t SOCKET PROGRAMING \t\t\t|
|\t SERVER NAME: {SERVER_NAME} \t\t\t|
|\t SERVER IP: {SERVER_IP} \t\t\t|
|                                                       |
|\t\t Đề 1: Tỷ Giá Vàng Việt Nam\t\t|
|                                                       |
|\t Authors: 19120557 - Trần Tuấn Kiệt\t\t|
|                                                       |
|_______________________________________________________|
'''


def help() -> str:
    return '''Important key words:
-quit: Exit program
-signin: Sign in
-signup: Sign up
'''


def log_in() -> str:
    return '''\nType "-signin" to sign in.
Type "-signup" to sign up.'''


def log_in_instruction(signin: bool = True) -> str:
    if signin:
        first_line = '_______________________SIGN IN_______________________'
        last_line = '\nOr you can create new account by typing: "-signup"'
    else:
        first_line = '_______________________SIGN UP_______________________'
        last_line = ''
    return f'''{first_line}
Type your username and your password (separate with a space " ")
For example: "MyName01 123456"{last_line}'''


def look_up_instruction() -> str:
    return '''_______________________LOOK UP_______________________
Type date and type (separate with a space " ")
For example: "2021-12-27 SJC"'''


def gold_info(l: list) -> str:
    s = f'{len(l)} results found:\n'
    for i in l:
        buy = i['buy']
        sell = i['sell']
        company = i['company']
        brand = i['brand']
        id = i['id']
        s += f''' _______________________
|BUY: {buy}\t\t|
|SELL: {sell}\t|
|Company: {company}\t|
|Brand: {brand}\t|
|ID: {id}\t\t|
|_______________________|
'''
    return s


def typo_error() -> str:
    return 'Typo error, please type again'


def combine(*kargs: str) -> str:
    s = ''
    for i in kargs:
        s += i
    return s
