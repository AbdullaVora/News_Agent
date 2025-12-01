import subprocess
import os

backend_path = os.path.join(os.getcwd(), "backend")
python_path = os.path.join(backend_path, "venv", "Scripts", "python.exe")

cmd = f'start cmd.exe /k "{python_path} main.py"'

subprocess.Popen(cmd, cwd=backend_path, shell=True)
