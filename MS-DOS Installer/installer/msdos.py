import os

def main(install_dir, __version__):
    os.chdir(install_dir)

    # Stato globale del programma
    state = {
        'current_dir': os.getcwd(),
        'default_dir': None,
        'settings': {}
    }

    DIGITS = '0123456789'
    OPERATORS = '+-*/'

    def clear():
        if os.name == 'nt':
            os.system("cls")
        else:
            os.system("clear")
    
    def load_preferences():
        pref_info = {}
        pref_file_path = os.path.join(install_dir, 'System', 'Preferences', 'preferences.txt')

        if os.path.exists(pref_file_path):
            with open(pref_file_path, 'r') as f:
                for line in f:
                    key, value = line.strip().split('=')
                    pref_info[key] = value
        return pref_info

    def load_settings():
        settings_info = {}
        settings_file_path = os.path.join(install_dir, 'System', 'Settings', 'settings.txt')

        if os.path.exists(settings_file_path):
            with open(settings_file_path, 'r') as f:
                for line in f:
                    key, value = line.strip().split('=')
                    settings_info[key] = value
        return settings_info

    def save_preferences(pref_info):
        pref_file_path = os.path.join(install_dir, 'System', 'Preferences', 'preferences.txt')
        with open(pref_file_path, 'w') as f:
            for key, value in pref_info.items():
                f.write(f"{key}={value}\n")

    def save_settings(settings_info):
        settings_file_path = os.path.join(install_dir, 'System', 'Settings', 'settings.txt')
        with open(settings_file_path, 'w') as f:
            for key, value in settings_info.items():
                f.write(f"{key}={value}\n")

    # Carica le preferenze e le impostazioni
    pref_info = load_preferences()
    state['settings'] = load_settings()
    state['default_dir'] = pref_info.get('defaultdir')

    if state['default_dir'] and os.path.isdir(state['default_dir']):
        os.chdir(state['default_dir'])
        state['current_dir'] = state['default_dir']

    def isExpr(line):
        result = 0
        tokens = line.split()

        if len(tokens) == 3 and tokens[0].isdigit() and tokens[2].isdigit() and tokens[1] in OPERATORS:
            num1 = float(tokens[0])
            num2 = float(tokens[2])
            operator = tokens[1]
            result = math(num1, operator, num2)
            return result
        elif len(tokens) == 1 and tokens[0] == 'dir':
            result = os.listdir()
            for i in result:
                print(i)
        elif len(tokens) == 1 and tokens[0] == 'cls':
            clear()
        elif len(tokens) == 2 and tokens[0] == 'cd':
            try:
                os.chdir(tokens[1])
                state['current_dir'] = os.getcwd()
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
        elif len(tokens) == 3 and tokens[0] == 'defaultdir' and tokens[1] == '=':
            new_dir = tokens[2]
            if os.path.isdir(new_dir):
                state['default_dir'] = new_dir
                state['current_dir'] = new_dir
                os.chdir(new_dir)
                pref_info['defaultdir'] = new_dir
                save_preferences(pref_info)
            else:
                print(f"Error: '{new_dir}' is not a valid directory.")
            return None
        elif len(tokens) == 2 and tokens[0] == 'nano':
            nano(tokens[1])
        elif len(tokens) == 3 and tokens[0] == 'settings' and tokens[1] == '=':
            key, value = tokens[2].split(':')
            state['settings'][key] = value
            save_settings(state['settings'])
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
        content = ""
        if os.path.exists(filename):
            clear()
            print(f"Opening file: {filename}")
            print("Use CTRL+C to save and exit\n\n")
            
            with open(filename, 'r') as file:
                content = file.read()
            print(content)
        
        try:
            while True:
                new_line = input()
                content += new_line + '\n'
        except KeyboardInterrupt:
            with open(filename, 'w') as file:
                file.write(content)
            print(f"\nFile '{filename}' saved.")

    clear()
    try:
        while True:
            line = input(f'{state["current_dir"]}>')
            result = isExpr(line)
            if result is not None:
                print(result)
    except KeyboardInterrupt:
        quit()
