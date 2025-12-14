# Ward Macro

A powerful and user-friendly macro automation tool for Windows, built with Python and CustomTkinter.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Features

- **Script Automation**: Create and manage multiple automation scripts
- **Trigger Options**: Execute scripts on interval or hotkey press
- **Screen Detection**: Check colors and read text (OCR) from screen regions
- **Mouse & Keyboard Control**: Simulate clicks, key presses, and text input
- **Profile System**: Save and load different script configurations
- **Code Editor**: Built-in Python editor with syntax highlighting and autocomplete
- **Multi-language**: Support for English and Portuguese

## Screenshots

*Coming soon*

## Installation

### Prerequisites

- Python 3.10 or higher
- Windows 10/11
- (Optional) Tesseract OCR for text recognition features

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ward-macro.git
cd ward-macro
```

### Step 2: Create Virtual Environment

```bash
python -m venv .venv
```

### Step 3: Activate Virtual Environment

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
python ward_macro.py
```

### (Optional) Install Tesseract OCR

For text recognition (OCR) features, install Tesseract:

1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to default location (`C:\Program Files\Tesseract-OCR`)
3. Restart Ward Macro

## Building Executable

To create a standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "WardMacro" --add-data "helpers;helpers" --add-data "ui;ui" ward_macro.py
```

The executable will be created in the `dist/` folder.

## Usage Guide

### Creating Your First Script

1. Launch Ward Macro
2. Click **"+ Add Script"**
3. Enter a script name
4. Choose trigger type:
   - **Interval**: Script runs repeatedly at specified milliseconds
   - **Hotkey**: Script runs when you press a specific key
5. Write your Python code using the available helpers
6. Click **Save**

### Available Helpers

#### Screen

```python
# Check if a position has a specific color
Screen.positionHasColor(x, y, "#FF0000")

# Check if a position has any of the colors
Screen.positionHasSomeColor(x, y, ["#FF0000", "#00FF00"])

# Get color at position
color = Screen.getColorAt(x, y)

# Extract text from area (requires Tesseract)
text = Screen.getAreaText(x1, y1, x2, y2)

# Check if area contains text
Screen.areaHasText(x1, y1, x2, y2, "search text")
```

#### Mouse

```python
# Click at position
Mouse.leftClick(x, y)
Mouse.rightClick(x, y)
Mouse.middleClick(x, y)
Mouse.doubleClick(x, y)

# Move cursor
Mouse.moveTo(x, y)
```

#### Keyboard

```python
# Press a single key
Keyboard.sendKey("enter")

# Press key combination
Keyboard.hotkey("ctrl", "c")

# Type text
Keyboard.typeText("Hello World", interval=0.05)
```

#### Sound

```python
# Play a beep sound
Sound.beep(frequency=1000, duration=200)
```

#### Debugger

```python
# Show color at position in a popup
Debugger.debugColor(x, y)

# Print text to logs panel
Debugger.printText("Script executed!")
```

### Using the Screen Capture Tool

1. Set your capture hotkey (default: `Ctrl+F12`)
2. Press the hotkey anywhere on screen
3. The coordinates and color will be captured
4. Click **Copy** buttons to copy values to clipboard

### Managing Profiles

- **Create Profile**: Type a name and click the `+` button
- **Switch Profile**: Select from the dropdown menu
- **Rename Profile**: Select profile, type new name, click rename button
- **Delete Profile**: Select profile and click delete button

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `F6` | Start/Stop all scripts |
| `Ctrl+F12` | Capture screen position (customizable) |
| `Ctrl+Z` | Undo (in code editor) |
| `Ctrl+Shift+Z` | Redo (in code editor) |
| `Ctrl+Space` | Trigger autocomplete |
| `Tab` | Insert indentation / Accept autocomplete |
| `Shift+Tab` | Remove indentation |
| `Escape` | Close autocomplete popup |

## Project Structure

```
ward_macro/
├── ward_macro.py          # Main application entry point
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── helpers/              # Helper classes for automation
│   ├── __init__.py
│   ├── screen.py         # Screen detection utilities
│   ├── keyboard.py       # Keyboard simulation
│   ├── mouse.py          # Mouse simulation
│   ├── sound.py          # Sound utilities
│   └── debugger.py       # Debugging tools
└── ui/                   # User interface components
    ├── __init__.py
    ├── area_selector.py  # Screen area selection overlay
    ├── code_editor.py    # Python code editor with autocomplete
    ├── script_modal.py   # Add/Edit script dialog
    ├── global_vars_modal.py  # Global variables editor
    ├── documentation_modal.py # Built-in documentation
    └── script_item.py    # Script list item widget
```

## Configuration

Ward Macro stores its configuration in `C:\WardMacro\`:

- `settings.json` - Application settings (language, etc.)
- `profiles.json` - List of profiles
- `profiles/` - Individual profile script files

## Contributing

We welcome contributions! Please follow these guidelines:

### Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/ward-macro.git
   ```
3. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. Make your changes
5. Test thoroughly
6. Commit with clear messages:
   ```bash
   git commit -m "Add: description of your feature"
   ```
7. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
8. Open a Pull Request

### Code Style Guidelines

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to new functions and classes
- Keep functions focused and concise
- Use type hints where appropriate

### Commit Message Format

Use prefixes to categorize your commits:

- `Add:` - New feature or file
- `Fix:` - Bug fix
- `Update:` - Update existing functionality
- `Remove:` - Remove code or files
- `Refactor:` - Code refactoring
- `Docs:` - Documentation changes
- `Style:` - Code style/formatting changes

### Pull Request Guidelines

- Provide a clear description of changes
- Reference any related issues
- Ensure all tests pass
- Update documentation if needed
- Keep PRs focused on a single feature/fix

### Reporting Issues

When reporting bugs, please include:

- Operating system and version
- Python version
- Steps to reproduce the issue
- Expected vs actual behavior
- Screenshots if applicable

### Feature Requests

We're open to new ideas! When suggesting features:

- Check if the feature already exists or was requested
- Describe the use case clearly
- Explain how it would benefit users

## Dependencies

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern UI framework
- [PyAutoGUI](https://pyautogui.readthedocs.io/) - GUI automation
- [Keyboard](https://github.com/boppreh/keyboard) - Hotkey handling
- [Pillow](https://pillow.readthedocs.io/) - Image processing
- [Pygments](https://pygments.org/) - Syntax highlighting
- [PyWin32](https://github.com/mhammond/pywin32) - Windows API access
- [psutil](https://psutil.readthedocs.io/) - Process utilities

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all contributors
- Inspired by various automation tools in the community

## Support

If you find this project useful, please consider:

- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 🤝 Contributing code


