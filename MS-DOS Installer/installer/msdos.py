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

def copy_file(source, destination):
    """ Copy the content of one file to another file. """
    try:
        with open(source, 'r') as src_file:
            content = src_file.read()
        
        with open(destination, 'w') as dest_file:
            dest_file.write(content)
        print(f"File '{source}' copied to '{destination}'.")
    except FileNotFoundError:
        print(f"Error: File '{source}' not found.")
    except IOError as e:
        print(f"Error: {e}")

def move_file(source, destination):
    """ Move a file from one location to another. """
    try:
        os.rename(source, destination)
        print(f"File '{source}' moved to '{destination}'.")
    except FileNotFoundError:
        print(f"Error: File '{source}' not found.")
    except IOError as e:
        print(f"Error: {e}")

def delete_file(filename):
    """ Delete a file. """
    try:
        os.remove(filename)
        print(f"File '{filename}' deleted.")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except IOError as e:
        print(f"Error: {e}")

def create_directory(directory):
    """ Create a new directory. """
    try:
        os.makedirs(directory, exist_ok=True)
        print(f"Directory '{directory}' created.")
    except OSError as e:
        print(f"Error: {e}")

def main(install_dir, __version__):
    global current_dir, default_dir, current_user, users  # Use global instead of nonlocal

    os.chdir(install_dir)
    current_dir = os.getcwd()

    settings_file_path = os.path.join(install_dir, 'System/Settings/settings.txt')
    users = load_users(settings_file_path)

    def clear():
        if os.name == 'nt':
            os.system("cls")
        else:
            os.system("clear")

    def load_pref_info():
        pref_info = {}
        pref_info_file_path = os.path.join(install_dir, 'System/Preferences/preferences.txt')

        if os.path.exists(pref_info_file_path):
            with open(pref_info_file_path, 'r') as f:
                for line in f:
                    key, value = line.strip().split('=')
                    pref_info[key] = value
        return pref_info

    def save_pref_info(defaultdir):
        """ Save preferences to a file. """
        pref_info_file_path = os.path.join(install_dir, 'System/Preferences/preferences.txt')
        with open(pref_info_file_path, 'w') as f:
            f.write(f"defaultdir={defaultdir}\n")
        print(f"Preferences saved: defaultdir set to {defaultdir}")

    pref_info = load_pref_info()
    default_dir = pref_info.get('defaultdir', install_dir)  # Set default_dir to install_dir if not set

    # Set the working directory to the loaded default_dir if it exists
    if os.path.isdir(default_dir):
        os.chdir(default_dir)
        current_dir = os.getcwd()
        print(f"Working directory set to defaultdir: {default_dir}")
    else:
        print(f"Error: The default directory '{default_dir}' does not exist. Using install directory.")
        os.chdir(install_dir)
        current_dir = os.getcwd()
        default_dir = install_dir  # Reset default_dir to install_dir

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
        tokens = line.split()

        if len(tokens) == 3 and tokens[0] == 'copy':
            source, destination = tokens[1], tokens[2]
            copy_file(source, destination)
        elif len(tokens) == 3 and tokens[0] == 'move':
            source, destination = tokens[1], tokens[2]
            move_file(source, destination)
        elif len(tokens) == 2 and tokens[0] == 'del':
            filename = tokens[1]
            delete_file(filename)
        elif len(tokens) == 2 and tokens[0] == 'mkdir':
            directory = tokens[1]
            create_directory(directory)
        elif len(tokens) == 2 and tokens[0] == 'cd':
            try:
                os.chdir(tokens[1])
                current_dir = os.getcwd()
                print(f"Changed directory to {current_dir}")
            except FileNotFoundError:
                print(f"Error: Directory '{tokens[1]}' not found.")
            except NotADirectoryError:
                print(f"Error: '{tokens[1]}' is not a directory.")
        elif len(tokens) == 1 and tokens[0] == 'dir':
            if current_user:
                result = os.listdir()
                for i in result:
                    print(i)
            else:
                print("You must be logged in to use this command.")
        elif len(tokens) == 1 and tokens[0] == 'cls':
            clear()
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
            new_dir = tokens[2]
            if not os.path.isabs(new_dir):
                new_dir = os.path.join(current_dir, new_dir)
            new_dir = os.path.abspath(new_dir)
            if os.path.isdir(new_dir):
                default_dir = new_dir
                os.chdir(default_dir)  # Change the current working directory
                current_dir = os.getcwd()  # Update the current directory to reflect the change
                save_pref_info(default_dir)  # Save the updated default directory to preferences
                print(f"Default directory set to: {default_dir}")
            else:
                print(f"Error: Directory '{tokens[2]}' not found or is not a directory.")
        else:
            print("Invalid expression format")

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
        for i, line in enumerate(content):
            print(f"{i + 1}: {line.strip()}")

        while True:
            print("\nType 'save' to save and exit, 'exit' to exit without saving.")
            input_line = input("nano> ").strip()

            if input_line.lower() == 'exit':
                print("Exiting without saving changes.")
                break
            elif input_line.lower() == 'save':
                with open(filename, 'w') as file:
                    file.writelines(content)
                print(f"File '{filename}' saved.")
                break
            else:
                # Assuming the input format is: <line_number> <new_content>
                tokens = input_line.split(maxsplit=1)
                if len(tokens) == 2:
                    line_number, new_content = tokens
                    if line_number.isdigit():
                        line_number = int(line_number)
                        if 1 <= line_number <= len(content):
                            content[line_number - 1] = new_content + '\n'
                        elif line_number == len(content) + 1:
                            content.append(new_content + '\n')
                        else:
                            print(f"Invalid line number. Please enter a number between 1 and {len(content) + 1}.")
                    else:
                        print("Invalid input. Please provide a line number followed by the new content.")
                else:
                    print("Invalid input format. Please provide a line number followed by the new content.")

    # Main loop
    while True:
        try:
            line = input(f"{current_user or 'Guest'}@{current_dir}> ")
            if line.strip().lower() == 'exit':
                print("Exiting MS-DOS Emulator.")
                break
            elif line.strip().lower().startswith('math'):
                tokens = line.split()
                if len(tokens) == 4:
                    num1 = int(tokens[1])
                    operator = tokens[2]
                    num2 = int(tokens[3])
                    result = math(num1, operator, num2)
                    print(f"Result: {result}")
                else:
                    print("Invalid math command format. Use: math <num1> <operator> <num2>")
            else:
                isExpr(line)
        except KeyboardInterrupt:
            print("\nExiting MS-DOS Emulator.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

