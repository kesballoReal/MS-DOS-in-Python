import os
import msdos
import setup

# Imposta la directory corrente
install_dir = os.getcwd() + "/MS-DOS"

current_dir = os.getcwd()
__version__ = None

# Funzione per caricare le informazioni di installazione da info.txt
def load_install_info():
    install_info = {}
    info_file_path = os.path.join(install_dir, 'info.txt')  # Percorso corretto per info.txt nella cartella MS-DOS

    if os.path.exists(info_file_path):
        with open(info_file_path, 'r') as f:
            for line in f:
                key, value = line.strip().split('=')
                install_info[key] = value
    return install_info

# Carica le informazioni di installazione
install_info = load_install_info()
is_installed = 'status' in install_info and install_info['status'] == 'installed'
install_path = install_info.get('install_path', install_dir)
__version__ = install_info.get('version', setup.__version__)

# Ciclo principale
while True:
    if is_installed:
        choice = input("Boot in MS-DOS? (Y/n): ").lower()
        if choice == 'y':
            msdos.main(install_dir, __version__)
    try:
        line = input(f"{current_dir}> ")
    except KeyboardInterrupt:
        print("\nExiting...")
        break

    if line == "setup" and not is_installed:
        setup.setup()
        install_info = load_install_info()  # Ricarica le informazioni di installazione
        is_installed = 'status' in install_info and install_info['status'] == 'installed'
        if is_installed:
            __version__ = install_info.get('version', setup.__version__)
    elif line == "setup" and is_installed:
        print(f"MS-DOS {__version__} is already installed.")      
    elif line == 'msdos' and is_installed:
        msdos.main(install_dir, __version__)       
    else:
        print(f"Error: command '{line}' not recognized.")
