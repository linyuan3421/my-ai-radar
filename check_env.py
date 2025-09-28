import sys
import site
import subprocess

print("--- Python Environment Diagnosis ---")
print(f"[*] Python Executable: {sys.executable}")
print(f"[*] Python Version: {sys.version.split()[0]}")
print("\n--- sys.path (Python's Search Paths) ---")
for i, path in enumerate(sys.path):
    print(f"  {i}: {path}")

print("\n--- Site-Packages Location ---")
print(f"[*] Main site-packages: {site.getsitepackages()}")

print("\n--- Checking for 'pymdownx' directly ---")
try:
    # We try to import a known module from the package
    import pymdownx.emoji
    print("[✔] SUCCESS: Successfully imported a module from 'pymdownx' package.")
    
    # Let's find out exactly where it's located
    location = pymdownx.__file__
    print(f"    Location of the package: {location}")
    
except ImportError as e:
    print(f"[✘] FAILURE: Failed to import. This is the root cause of the error.")
    print(f"    Error details: {e}")

print("\n--- Verifying mkdocs installation ---")
try:
    # Check where mkdocs is installed
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'show', 'mkdocs'],
        capture_output=True, text=True, check=True
    )
    print(result.stdout)
except Exception as e:
    print(f"[✘] FAILURE: Could not get info for mkdocs. Error: {e}")
    
print("--- Diagnosis Complete ---")