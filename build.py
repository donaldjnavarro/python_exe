import subprocess
import re
import os
from packaging import version
import shutil

DIST_DIR = "dist"
EXE_BASE_NAME = "main"
VERSIONED_PREFIX = "main_v"
MAIN_SCRIPT = "main.py"
SPEC_FILE = f"{EXE_BASE_NAME}.spec"

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
    # Always build with fixed name 'main' to reuse spec file
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name", EXE_BASE_NAME,
        MAIN_SCRIPT
    ]
    print(f"Building EXE with fixed name '{EXE_BASE_NAME}.exe'")
    subprocess.run(cmd, check=True)

def main():
    latest_ver = find_latest_version()
    if latest_ver is None:
        new_version = "1.0.0"
    else:
        new_version = increment_patch(latest_ver)
    
    build_exe()
    
    # Rename the generated EXE to versioned name
    src = os.path.join(DIST_DIR, f"{EXE_BASE_NAME}.exe")
    dst = os.path.join(DIST_DIR, f"{VERSIONED_PREFIX}{new_version}.exe")
    
    print(f"Renaming {src} -> {dst}")
    shutil.move(src, dst)
    
    print(f"Build complete: version {new_version}")

if __name__ == "__main__":
    main()
