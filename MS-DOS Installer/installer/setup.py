import datetime as dt
import time as tm
import os
import shutil

time = dt.datetime.now()
if os.name == 'nt':
    path_to_install = "C:"
    os.chdir("C://")
else:
    path_to_install = "/"
    os.chdir("/")
install_path = ""
total, used, free = shutil.disk_usage("/")



__version__  = 1.0


def clear():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")

def setup1():
    clear()
    print(f"Microsoft MS-DOS {__version__} Setup\n\n")
    print(f"Welcome to MS-DOS {__version__} Setup.")
    print(f"\nThis wizard will help you to install MS-DOS {__version__} onto your system.")
    print("\nPlease press 1 to continue, or 2 to close this wizard.")
    print("\n(C)Copyright Microsoft Corp 1981-1999.")
    print("\n1) Next")
    print("2) Cancel")
    setupchoice = int(input())

    if setupchoice == 1:
        clear()
        print(f"Microsoft MS-DOS {__version__} Setup\n\n")
        print("MS-DOS is the most widely-used and useful DOS today.")
        print("It fully supports large hard disks, FAT12/16/32 drives, Long File Names (LFN), large memoery, Windows GUI, etc.")
        print(f"\nMS-DOS {__version__} will provide you with a lot of new features, and you will gain a lot of new experiences.")

        print("\n1) Next")
        print("2) Cancel")

        setupchoice = int(input())

        if setupchoice == 1:
            clear()
            print(f"Microsoft MS-DOS {__version__} Setup\n\n")
            print("Setup needs to configure the unallocated space on your hard disk for use with MS-DOS.\nTo have Setup configure the space for you, choose the reccomended option.")
            print("\n1)Configure unallocated disk space (reccomended).")
            print("2)Exit Setup.")

            option = int(input())

            if option == 1:
                clear()
                print(f"Microsoft MS-DOS {__version__} Setup\n\n")
                print("Setup will restart your computer now..")
                tm.sleep(1)
                setup2()
            elif option == 2:
                quit()

def setup2():
    global install_path
    
    clear()
    print("BIOS(C) 1998 Inc.")
    print("\nPress DEL to run Setup")
    print("Checking NVRAM..")
    print("\n64MB OK")
    print("Auto-Detecting Pri Channel (0)... IDE Hard Disk")
    print("Auto-Detecting Pri Channel (1)... Not Detected")
    print("Auto-Detecting Sec Channel (0)... CDROM")
    print("Auto-Detecting Sec Channel (1)... Not Detected")

    tm.sleep(3)

    clear()
    print("Starting MS-DOS...")

    tm.sleep(2)

    clear()
    print(f"Microsoft MS-DOS {__version__} Setup\n\n")
    print(f"Setup will install MS-DOS {__version__} in the following path: {path_to_install}")
    print("\nTo install to a different path, please insert here the new path (Ex: 'C:', '/') We reccommend 'C' or '/': ")
    newpath = str(input("New Path: "))

    if os.path.exists(newpath):
        # Appending "/DOS1" to the new path
        install_path = os.path.join(newpath, "MS-DOS")

        # Create the target directory if it doesn't exist
        os.makedirs(install_path, exist_ok=True)

        total, used, free = shutil.disk_usage(newpath)

        print(f"\nMS-DOS Path: {install_path}")
        print("\nTotal Space: %d GiB" % (total // (2**30)))
        print("Used Space: %d GiB" % (used // (2**30)))
        print("Free Space: %d GiB" % (free // (2**30)))

    else:
        print(f"\nPath '{newpath}' does not exist. Please insert a correct path.")
        quit()

    print("\n1) Next")
    print("2) Cancel")
    setupchoice = int(input())

    if setupchoice == 1:
        clear()
        
        # Absolute path to the source directory
        source_dir = os.path.join(os.path.dirname(__file__), 'installer')
        
        # Check if source_dir exists
        if not os.path.exists(source_dir):
            print(f"Source directory '{source_dir}' does not exist.")
            quit()
        
        shutil.copytree(source_dir, install_path, dirs_exist_ok=True)

        with open(os.path.join(install_path, 'info.txt'), 'w') as f:
            f.write(f"install_path={install_path}\n")
            f.write("status=installed\n")
            f.write(f"version={__version__}")

        
        print(f"\nMS-DOS {__version__} has been successfully installed in {install_path}!")
        tm.sleep(2)



def setup():
    print("------------------------------------------------------------")
    print(f"MS-DOS {__version__} Installation CD Menu                   5 = Help")
    print("------------------------------------------------------------")
    print(f"\n1) Install MS-DOS 1{__version__} [Enter]")
    print("\n2) Boot from Floppy Drive")
    print("\n3) Boot from Hard Drive")
    choice = input("\n\nHit the key of choice: ")

    if choice == "":
        print(f"Now loading MS-DOS {__version__} Installation Disk...")
        print("Running DOS1INS.IMG")
        print("Emulating CHS 80/9/2")
        print(f"Starting MS-DOS {__version__}...")

        print(f"\nIDE/ATAP CD-ROM Device Driver    Version 2.14    {time}")
        tm.sleep(1)
        setup1()

