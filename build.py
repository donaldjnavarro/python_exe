import subprocess
import re
import os
from packaging import version
import shutil
import sys

DIST_DIR = "dist"
EXE_BASE_NAME = "main"
VERSIONED_PREFIX = "main_v"
MAIN_SCRIPT = "main.py"

def find_latest_version():
    if not os.path.exists(DIST_DIR):
        return None

    semver_pattern = re.compile(rf"{re.escape(VERSIONED_PREFIX)}(\d+\.\d+\.\d+)\.exe")
    versions_found = []

    for fname in os.listdir(DIST_DIR):
        m = semver_pattern.match(fname)
        if m:
            ver_str = m.group(1)
            try:
                ver = version.parse(ver_str)
                versions_found.append(ver)
            except Exception:
                pass

    if not versions_found:
        return None

    return max(versions_found)

def increment_patch(ver):
    major = ver.major
    minor = ver.minor
    patch = ver.micro + 1
    return f"{major}.{minor}.{patch}"

def build_exe():
    import en_core_web_sm
    model_path = os.path.dirname(en_core_web_sm.__file__)
    stopwords_path = "utils/spacy_stopwords.py"

    # Format --add-data arguments based on OS
    if os.name == 'nt':  # Windows
        data_args = [
            f"{model_path};en_core_web_sm",
            f"{stopwords_path};utils"
        ]
    else:
        data_args = [
            f"{model_path}:en_core_web_sm",
            f"{stopwords_path}:utils"
        ]

    cmd = [
        "pyinstaller",
        "--onefile",
        "--noconsole",
        "--exclude-module=tkinter",
        "--name", EXE_BASE_NAME,
        MAIN_SCRIPT,
        "--hidden-import=docx",
        "--hidden-import=en_core_web_sm",
    ]

    # Add --add-data for each path
    for data_arg in data_args:
        cmd.extend(["--add-data", data_arg])

    print(f"Building EXE with fixed name '{EXE_BASE_NAME}.exe'")
    subprocess.run(cmd, check=True)

def main():
    latest_ver = find_latest_version()
    if latest_ver is None:
        new_version = "1.0.0"
    else:
        new_version = increment_patch(latest_ver)

    # Run generate_stopwords.py to update the stopwords file before build
    print("Generating stopwords file from SpaCy...")
    subprocess.run([sys.executable, "utils/generate_stopwords.py"], check=True)

    build_exe()

    # Rename the generated EXE to versioned name
    src = os.path.join(DIST_DIR, f"{EXE_BASE_NAME}.exe")
    dst = os.path.join(DIST_DIR, f"{VERSIONED_PREFIX}{new_version}.exe")

    print(f"Renaming {src} -> {dst}")
    shutil.move(src, dst)

    print(f"Build complete: version {new_version}")

if __name__ == "__main__":
    main()
