import os
import hashlib  # To hash passwords

# Move these variables outside of the `main` function
current_dir = None
default_dir = None
current_user = None  # Track the currently logged-in user
users = {}

def hash_password(password):
    """ Hash a password for storing. """
    return hashlib.sha256(password.encode()).hexdigest()

def load_users(file_path):
    """ Load users from a settings file. """
    if not os.path.exists(file_path):
        return {}
    
    with open(file_path, 'r') as file:
        users = {}
        for line in file:
            if line.strip():
                username, hashed_password = line.strip().split(':')
                users[username] = hashed_password
        return users

def save_user(file_path, username, hashed_password):
    """ Save a new user to the settings file. """
    with open(file_path, 'a') as file:
        file.write(f"{username}:{hashed_password}\n")

def main(install_dir, __version__):
    global current_dir, default_dir, current_user, users  # Use global instead of nonlocal

    os.chdir(install_dir)
    current_dir = os.getcwd()

    DIGITS = '0123456789'
    OPERATORS = '+-*/'

    settings_file_path = os.path.join(install_dir, 'System/Settings/settings.txt')
    users = load_users(settings_file_path)

    def clear():
        if os.name == 'nt':
            os.system("cls")
        else:
            os.system("clear")

    def load_pref_info():
        pref_info = {}
        pref_info_file_path = os.path.join(install_dir, 'Preferences/preferences.txt')

        if os.path.exists(pref_info_file_path):
            with open(pref_info_file_path, 'r') as f:
                for line in f:
                    key, value = line.strip().split('=')
                    pref_info[key] = value
        return pref_info

    pref_info = load_pref_info()
    default_dir = pref_info.get('defaultdir')

    def login(username, password):
        global current_user
        hashed_password = hash_password(password)
        if username in users and users[username] == hashed_password:
            current_user = username
            print(f"Welcome, {username}!")
        else:
            print("Invalid username or password.")

    def logout():
        global current_user
        if current_user:
            print(f"Goodbye, {current_user}!")
            current_user = None
        else:
            print("No user is currently logged in.")

    def create_user(username, password):
        if username in users:
            print(f"User '{username}' already exists.")
        else:
            hashed_password = hash_password(password)
            users[username] = hashed_password
            save_user(settings_file_path, username, hashed_password)
            print(f"User '{username}' created successfully.")

    def isExpr(line):
        global current_dir, default_dir  # Use global instead of nonlocal
        result = 0
        tokens = line.split()

        if len(tokens) == 3 and tokens[0].isdigit() and tokens[2].isdigit() and tokens[1] in OPERATORS:
            num1 = float(tokens[0])
            num2 = float(tokens[2])
            operator = tokens[1]
            result = math(num1, operator, num2)
            return result
        elif len(tokens) == 1 and tokens[0] == 'dir':
            if current_user:
                result = os.listdir()
                for i in result:
                    print(i)
            else:
                print("You must be logged in to use this command.")
        elif len(tokens) == 1 and tokens[0] == 'cls':
            clear()
        elif len(tokens) == 2 and tokens[0] == 'cd':
            try:
                os.chdir(tokens[1])
                current_dir = os.getcwd()
            except FileNotFoundError:
                print(f"Error: Directory '{tokens[1]}' not found.")
            except NotADirectoryError:
                print(f"Error: '{tokens[1]}' is not a directory.")
            return None
        elif len(tokens) == 1 and tokens[0] == 'ver':
            print(f"Microsoft(C) MS-DOS {__version__}")
        elif len(tokens) >= 2 and tokens[0] == 'print':
            message = ' '.join(tokens[1:])
            print(message)
        elif len(tokens) == 2 and tokens[0] == 'nano':
            if current_user:
                nano(tokens[1])
            else:
                print("You must be logged in to use this command.")
        elif len(tokens) == 3 and tokens[0] == 'login':
            username = tokens[1]
            password = tokens[2]
            login(username, password)
        elif len(tokens) == 1 and tokens[0] == 'logout':
            logout()
        elif len(tokens) == 4 and tokens[0] == 'createuser':
            username = tokens[1]
            password = tokens[2]
            confirm_password = tokens[3]
            if password == confirm_password:
                create_user(username, password)
            else:
                print("Passwords do not match.")
        elif len(tokens) == 3 and tokens[0] == 'defaultdir' and tokens[1] == '=':
            try:
                default_dir = tokens[2]
                current_dir = default_dir
            except FileNotFoundError:
                print(f"Error: Directory '{tokens[2]}' not found.")
            except NotADirectoryError:
                print(f"Error: '{tokens[2]}' is not a directory.")
            return None
        else:
            print("Invalid expression format")
            return None

    def math(num1, operator, num2):
        result = 0
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            try:
                result = num1 / num2
            except ZeroDivisionError:
                result = None
                print("Error: Division by Zero!")
        return result

    def nano(filename):
        # Check if file exists and read its content
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                content = file.readlines()
        else:
            content = []    

        clear()
        print(f"Opening file: {filename}")
        print("Use commands to navigate and edit the file.")
        print("Commands: ':w <text>' to write/replace line, ':d' to delete current line, ':p' to go to the previous line, ':n' to go to the new line, ':q' to save and exit.\n")

        current_line = 0

        # Main loop for editing the file
        while True:
            if current_line < 0:
                current_line = 0
            if current_line >= len(content):
                current_line = len(content) - 1

            if content:
                print(f"{current_line + 1}: {content[current_line]}", end='')  # Display current line
            else:
                print(f"{current_line + 1}: ")

            command = input("Command> ")

            if command.startswith(':q'):
                # Save and exit
                with open(filename, 'w') as file:
                    file.writelines(content)
                print(f"File '{filename}' saved.")
                break
            elif command.startswith(':w '):
                # Write/Replace current line
                _, text = command.split(' ', 1)
                if current_line >= 0 and current_line < len(content):
                    content[current_line] = text + '\n'
                else:
                    content.append(text + '\n')
            elif command == ':d':
                # Delete current line
                if content:
                    content.pop(current_line)
                if current_line >= len(content):
                    current_line = len(content) - 1
            elif command.startswith(':s '):
                # Search for text
                _, search_text = command.split(' ', 1)
                found = False
                for i, line in enumerate(content):
                    if search_text in line:
                        current_line = i
                        found = True
                        break
                if not found:
                    print(f"'{search_text}' not found.")
            elif command == ':n':
                # Go to the next line
                current_line += 1
            elif command == ':p':
                # Go to the previous line
                current_line -= 1
            else:
                print("Invalid command. Use ':w <text>', ':d', ':s <text>', ':n', ':p'.")

    clear()
    try:
        while True:
            line = input(f'{current_dir}>')
            result = isExpr(line)
            if result is not None:
                print(result)
    except KeyboardInterrupt:
        quit()
