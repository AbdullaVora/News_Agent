import subprocess
import os
import sys

backend_path = os.path.join(os.getcwd(), "backend")
frontend_path = os.path.join(os.getcwd(), "frontend")

python_path = os.path.join(backend_path, "venv", "Scripts", "python.exe")

print("Starting Backend server.py using venv Python:", python_path)
subprocess.Popen([python_path, "server.py"], cwd=backend_path)

print("Starting Frontend (React)...")
# On Windows, use shell=True to locate npm automatically
subprocess.Popen("npm run dev", cwd=frontend_path, shell=True)

print("GUI started!")
