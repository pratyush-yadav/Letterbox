import os
from datetime import datetime
from getpass import getpass
from time import sleep
from random import randrange


def check_and_start():
    data_path = os.path.join(os.getcwd(), 'Data')
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    os.chdir(data_path)
    with open('usd.txt', 'at'):
        pass
    with open('usd.txt', 'rt') as f:
        a = f.read()
        a = a.split('||~||')
    if len(a) == 1:
        with open('usd.txt', 'wt') as f:
            # dummy login details for admin...
            # Name : Administrator
            # User ID : admin
            # Password : admin123
            f.write(f'Administrator~~|~~admin~~|~~admin123~~|~~{get_time()}')
            # throughout this code, '||~||' is used to separate rows and '~~|~~' is used to separate columns.
    welcome_page()


def clear(text=''):
    os.system('cls')
    print()
    print("@@@@@_____LETTERBOX_____@@@@@".center(80))
    print('\n')
    print(f"_____ {text} _____".center(80))
    print('\n\n')


def get_time(username=None):
    if username is None:
        return datetime.now().strftime('%Y%m%d%H%M%S%f')
    else:
        with open('usd.txt', 'rt') as f:
            a = f.read()
            a = a.split('||~||')
            for i in a:
                i = i.split('~~|~~')
                if i[1] == username:
                    return i[-1]


def get_usernames():
    usernames = []
    with open('usd.txt', 'rt') as f:
        a = f.read()
        a = a.split('||~||')
        for i in a:
            i = i.split('~~|~~')
            try:
                usernames.append(i[1])
            finally:  # cannot use except block because it required a compulsory exception.
                pass
        usernames.sort()
        return usernames


def get_password(username):
    with open('usd.txt', 'rt') as f:
        a = f.read()
        a = a.split('||~||')
        for i in a:
            i = i.split('~~|~~')
            if i[1] == username:
                return i[2]


def get_name(username):
    with open('usd.txt', 'rt') as f:
        a = f.read()
        a = a.split('||~||')
        for i in a:
            i = i.split('~~|~~')
            if i[1] == username:
                return i[0]


def welcome_user_page(username):
    clear(f'Welcome {get_name(username)} ({username})')
    print('\n1. View / select user\n\n2. Account settings\n\n3. Exit\n')
    i = input('>>> ')
    if i == '1':
        select_recipient(username)
    elif i == '2':
        account_settings(username)
    elif i == '3':
        welcome_page()
    else:
        print('Invalid Input!')
        sleep(1)
        welcome_user_page(username)


def select_recipient(username):
    while True:
        clear(f'Welcome {get_name(username)} ({username})')
        usernames = get_usernames()
        count = 0
        for i in usernames:
            if not (i == 'admin' or i == username):
                print(i.center(21), end='')
                count += 1
            if count % 4 == 0:
                print()
        print('\n\n')
        print('(Leave this field empty and press enter to cancel/exit.)\n')
        recipient = input("Enter Recipient's username: ")
        if recipient == '':
            welcome_user_page(username)
        elif recipient in get_usernames():
            view_conversation(username, recipient)
            break
        else:
            print('Invalid Username!')
            sleep(1)


def send_message(username, recipient):
    clear(f"Welcome {get_name(username)} ({username})")
    print(f"\nRecipient: {get_name(recipient)} ({recipient})\n\n")
    print("Compose message:\n")
    message = input()
    clear()
    if not message.isspace() and message != '':
        with open(get_time(username) + '.txt', 'at') as f:
            f.write('||~||')
            f.write(f"{username}~~|~~{recipient}~~|~~{message}~~|~~{get_time()}")
        with open(get_time(recipient) + '.txt', 'at') as f:
            f.write('||~||')
            f.write(f"{username}~~|~~{recipient}~~|~~{message}~~|~~{get_time()}")
    clear()
    view_conversation(username, recipient)


def view_conversation(username, recipient):
    with open(get_time(recipient) + '.txt', 'rt') as f:
        a = f.read()
        a = a.split('||~||')
        clear(f"Welcome {get_name(username)} ({username})")
        print(f"Recipient {get_name(recipient)} ({recipient}) selected\n\n")
        for i in a:
            i = i.split('~~|~~')
            if i[0] == recipient and i[1] == username:
                print(f'\n{get_name(recipient)}:  ', i[2])
            elif i[0] == username and i[1] == recipient:
                print(f'\n{get_name(username)}:  ', i[2])
        i = input('\n\n1. Refresh\n2. Send message\n3. Exit\n\n>>> ')
        if i == '1':
            view_conversation(username, recipient)
        elif i == '2':
            send_message(username, recipient)
        elif i == '3':
            welcome_user_page(username)
        else:
            view_conversation(username, recipient)


def account_settings(username):
    while True:
        clear(f"Welcome {get_name(username)} ({username})")
        print("Account Settings")
        i = input("\n1. Change password\n\n2. Exit\n\n>>> ")
        if i == '1':
            change_password(username)
        elif i == '2':
            welcome_user_page(username)
        else:
            print('(Invalid Input!)')
            sleep(1)
            continue


def change_password(username):
    while True:
        clear(f"***** Change Password *****")
        print('Name:', get_name(username))
        print('\nUser ID:', username)
        print("\n(Min 5 , Max 20 characters)")
        print("(Password won't be visible while typing!)\n")
        old_p_input = getpass("Enter old password: ")
        if old_p_input != get_password(username) or old_p_input == '':
            print("Incorrect password!")
            print("\nPassword Change Cancelled!")
            sleep(1)
            welcome_user_page(username)
        else:
            new_p_input = getpass("Set new password: ")
            if new_p_input == '':
                print("\nPassword Change Cancelled!")
                sleep(1)
                welcome_user_page(username)
            elif len(new_p_input) < 5:
                print('New password is Too Short!')
                sleep(1)
                continue
            elif len(new_p_input) > 20:
                print('New password is Too Long!')
                sleep(1)
                continue
            elif ' ' in new_p_input:
                print('Password Cannot contain Space!')
                sleep(1)
                continue
            else:
                old = f"{get_name(username)}~~|~~{username}~~|~~{old_p_input}~~|~~{get_time(username)}"
                new = f"{get_name(username)}~~|~~{username}~~|~~{new_p_input}~~|~~{get_time(username)}"
                with open('usd.txt', 'rt') as f:
                    a = f.read()
                a = a.replace(old, new)
                with open('usd.txt', 'wt') as f:
                    f.write(a)
                clear(f"***** Change Password *****")
                print('Name:', get_name(username))
                print('\nUser ID:', username)
                print('\nNew Password:', '*' * len(new_p_input))
                input('\nPassword Changed Successfully!\n\nPress enter to continue...\n')
                welcome_user_page(username)


def forgot_password(username):
    def update_password_in_file(new_password):
        old = f"{get_name(username)}~~|~~{username}~~|~~{get_password(username)}~~|~~{get_time(username)}"
        new = f"{get_name(username)}~~|~~{username}~~|~~{new_password}~~|~~{get_time(username)}"
        with open('usd.txt', 'rt') as fr:
            a = fr.read()
        a = a.replace(old, new)
        with open('usd.txt', 'wt') as fw:
            fw.write(a)
        clear('Forgot password')
        print('Username:', username)
        print('Password:', '*' * len(new_password))
        print('Password Changed Successfully')
        sleep(1)
        welcome_page()
    while True:
        clear('***** Forgot Password *****')
        print('Username:', username)
        print("\nA message will be sent to the Administrator containing your username and OTP. \
In order to reset your password, you need to contact the Administrator \
and ask for your OTP and enter it in the field below.")
        i = input('\nDo you wish to continue?\n1. Yes\n2. No\n\n>>> ')
        if i == '1':
            with open(get_time(username) + '.txt', 'at') as f:
                f.write('||~||')
                r = str(randrange(1000, 9999))
                t = f'{username}~~|~~admin~~|~~OTP to reset my account password is {r}~~|~~{get_time()}'
                f.write(t)
            for _ in range(3):
                clear('***** Forgot Password *****')
                print('Username:', username)
                otp = input('\nEnter OTP: ')
                if otp == r:
                    while True:
                        clear('***** Forgot Password *****')
                        print('Username:', username)
                        print("\n(Password won't be visible while typing.)")
                        print("(Min 5 , Max 20 characters)\n")
                        input_new_password = getpass('Enter New Password: ')
                        if input_new_password == '':
                            break
                        elif len(input_new_password) < 5:
                            print('(Too Short!)')
                            sleep(1)
                            continue
                        elif len(input_new_password) > 20:
                            print('(Too Long!)')
                            sleep(1)
                            continue
                        elif ' ' in input_new_password:
                            print("Password cannot contain space!")
                            sleep(1)
                            continue
                        else:
                            update_password_in_file(input_new_password)

                else:
                    print('(Incorrect OTP)')
                    sleep(1)
            else:
                print("Try again after sometime!")
                sleep(1)
                welcome_page()
        elif i == '2':
            welcome_page()
        else:
            print('Invalid Input!')
            sleep(1)
            forgot_password(username)


def welcome_page():
    while True:
        clear(" Welcome to LETTERBOX ")
        print("Help: Type the number and press enter to select the option displayed against it.\n\n")
        i = input("1: Login\n2: Register\n\n3: Quit\n\n>>> ")
        if i == '1':
            login_page()
        elif i == '2':
            signup_page()
        elif i == '3':
            exit_page()
        else:
            print('Invalid Input!')
            sleep(1)
            continue


def login_page():
    while True:
        clear('LOG IN')
        username = input('Enter User ID: ')
        if username == '':
            welcome_page()
        elif username not in get_usernames():
            print('User does not exists!')
            sleep(1)
            continue
        else:
            break
    password = get_password(username)
    count = 0
    while True:
        clear('LOG IN')
        print('Username:', username)
        print("\n(password won't be displayed while typing.)\n")
        input_password = getpass('Enter password: ')
        clear('LOG IN')
        print('Username:', username)
        print('Password:', '*' * len(input_password))
        count += 1
        if input_password == password:
            print('\n\nLogin Successful...')
            sleep(1)
            welcome_user_page(username)
        elif count >= 3:
            i = ''
            while i not in ['1', '2', '3']:
                clear('LOG IN')
                print('Username:', username)
                print('Password:', '*' * len(input_password))
                i = input('\n\nIncorrect password!\n\n1: Try again\n2: Forgot password\n3: Exit\n\n')
            if i == '1':
                continue
            elif i == '2':
                pass
                forgot_password(username)
            elif i == '3':
                welcome_page()
        else:
            print('Incorrect Password!')
            sleep(1)


def signup_page():
    def input_name():
        clear('SIGN UP')
        print("(Min 5 , Max 20 characters)\n")
        name_input = input('Enter your name: ')
        if input_name == '':
            welcome_page()
        elif len(name_input) < 5:
            print('(Name is Too Short!)')
            sleep(1)
            return input_name()
        elif len(name_input) > 20:
            print('(Name is Too Long!)')
            sleep(1)
            return input_name()
        for c in name_input:
            if not (c.isalpha() or c.isspace()):
                print("Name should only contain Alphabets and Space.")
                return input_name()
        return name_input.title()

    def input_id():
        clear('SIGN UP')
        print('Name:', name)
        print("\n(Min 5 , Max 20 characters)\n")
        input_user = input('Set User ID: ')
        if input_user == '':
            welcome_page()
        elif len(input_user) < 5:
            print('(Too Short!)')
            sleep(1)
            return input_id()
        elif len(input_user) > 20:
            print('(Too Long!)')
            sleep(1)
            return input_id()
        elif input_user in get_usernames():
            print('(This ID is taken, Try something else.)')
            sleep(1)
            return input_id()
        for c in input_user:
            if not (c.isalpha() or c.isdigit()):
                print("Only alphabets and digits allowed in User ID.")
                return input_id()
        return input_user

    def input_password():
        clear('SIGN UP')
        print('Name:', name)
        print('\nUser ID:', username)
        print("\n(Password won't be visible while typing.)")
        print("(Min 5 , Max 20 characters)\n")
        ip_password = getpass("Set password: ")
        if ip_password == '':
            welcome_page()
        elif len(ip_password) < 5:
            print('(Too Short!)')
            sleep(1)
            return input_password()
        elif len(ip_password) > 20:
            print('(Too Long!)')
            sleep(1)
            return input_password()
        elif ' ' in ip_password:
            return input_password()
        else:
            return ip_password

    name = input_name()
    username = input_id()
    password = input_password()
    confirm = ''
    while confirm not in ('1', '2'):
        clear('SIGN UP')
        print('Name:', name)
        print('\nUser ID:', username)
        print('\nPassword:', '*' * len(password))
        confirm = input('\n\n1: Register\n2: Cancel\n')
        if confirm == '1':
            time = get_time()
            register = f"{name}~~|~~{username}~~|~~{password}~~|~~{time}"
            with open('usd.txt', 'at') as f:
                f.write('||~||')
                f.write(register)
            with open(time + '.txt', 'wt'):
                pass
            clear('SIGN UP')
            print('Name:', name)
            print('\nUser ID:', username)
            print('\nPassword:', '*' * len(password))
            input('\n\nRegistration Successful!\n\nPress enter to continue...\n')
            welcome_page()
        elif confirm == '2':
            clear('SIGN UP')
            print('Name:', name)
            print('\nUser ID:', username)
            print('\nPassword:', '*' * len(password))
            input('\n\nRegistration Cancelled!\n\nPress enter to continue...\n')
            welcome_page()


def exit_page():
    clear('_____')
    print('ThankYou! Visit Again...\n\n')
    sleep(2)
    quit()


check_and_start()
