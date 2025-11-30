import subprocess
import os

backend_path = os.path.join(os.getcwd(), "backend")
python_path = os.path.join(backend_path, "venv", "Scripts", "python.exe")

print("Starting CLI (main.py) using venv Python:", python_path)
subprocess.Popen([python_path, "main.py"], cwd=backend_path)

print("CLI started!")
