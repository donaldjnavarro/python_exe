# EXE TEMPLATE PROJECT

## Getting Started

### Launch Virtual Environment

```bash
.\venv\Scripts\activate
```

### Create new EXE

Build command with versioning:

```bash
python build.py
```

Deprecated build command:
~~pyinstaller --onefile main.py~~

## Framework Overview

### Architecture

`main.py` The main python file

`main.spec` Config file for the EXE compiler

`build.py` Handles the versioning and other particulars of new EXE builds

`dist/` Where new EXEs will be created

`requirements.txt` pip package manager config

### Tools

* **Package manager**: PIP
* **EXE**: PyInstaller
* **UI**: wxPython
