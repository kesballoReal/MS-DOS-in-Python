# MS-DOS Python Emulator

This project simulates a basic MS-DOS environment using Python scripts. It includes a command-line interface that allows for basic file operations, directory navigation, and arithmetic computations. This emulator can be run in a Python environment and is designed to be as simple and interactive as possible.

## Features

- **Command-line Interface**: Simulates MS-DOS commands.
- **Basic Arithmetic**: Perform arithmetic operations.
- **File Operations**: List directories, change directories, and edit files using a simple text editor.
- **Preferences**: Load preferences and set default directories.

## Prerequisites

- Python 3.x
- Basic understanding of command-line operations.

## Installation

1. **Clone the Repository or Download and extract the zip file.**

   ```bash
   git clone https://github.com/kesballoReal/MS-DOS-in-Python
   cd msdosproject
   ```

2. **Set Up the Project**

   Ensure you have Python 3 installed. No additional dependencies are required beyond the standard library for this project.

## Usage

1. **Navigate to the Project Directory**

   ```bash
   cd /path/to/msdosproject
   ```

2. **Run the Python Script**

   ```bash
   sudo python3 boot.py
   ```
   or

   ```bash
   python boot.py
   ```
   This will start the MS-DOS emulator. You will see a command prompt where you can enter commands.
   Type in the console
   
   ```bash
   setup
   ```
   to start the Setup

   

## Commands

- **`dir`**: List files and directories in the current directory.
- **`cd <directory>`**: Change the current directory.
- **`cls`**: Clear the terminal screen.
- **`ver`**: Display version information.
- **`print <message>`**: Print a message to the terminal.
- **`nano <filename>`**: Open a file in a simple text editor. If the file does not exist, it will be created.
- **`defaultdir=<directory>`**: Set a new default directory. This will change the starting directory for the next session.

## Preferences

Preferences can be set in the `Preferences/preferences.txt` file. For example:

```
defaultdir=/path/to/default/dir
```

## Development

To contribute to this project:

1. **Fork the Repository** on GitHub.
2. **Clone your fork**:

   ```bash
   git clone https://github.com/kesballoReal/msdosproject.git
   ```

3. **Create a Branch** for your changes:

   ```bash
   git checkout -b feature/your-feature
   ```

4. **Make Changes** and **Commit**:

   ```bash
   git add .
   git commit -m "Add new feature"
   ```

5. **Push Changes**:

   ```bash
   git push origin feature/your-feature
   ```

6. **Create a Pull Request** on GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by classic MS-DOS environments.
- Thanks to the open-source community for their support and tools.
