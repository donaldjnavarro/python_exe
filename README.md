# EXE TEMPLATE PROJECT

Provides an EXE file for an app that analyzes text and gives some metrics and visualization to give writers perspective on their writing.

## Getting Started

### Launch Virtual Environment

```bash
.\venv\Scripts\activate
```

### Run without EXE

```bash
python main.py
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
