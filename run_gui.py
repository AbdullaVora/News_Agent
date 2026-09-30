import subprocess
import os
import sys

root_path = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(root_path, "backend")
frontend_path = os.path.join(root_path, "frontend")

# Look for Python executable in root venv, backend venv, or current python interpreter
candidates = [
    os.path.join(root_path, "venv", "Scripts", "python.exe"),
    os.path.join(backend_path, "venv", "Scripts", "python.exe"),
    os.path.join(root_path, "venv", "bin", "python"),
    os.path.join(backend_path, "venv", "bin", "python"),
    sys.executable,
]

python_path = None
for candidate in candidates:
    if os.path.isfile(candidate):
        python_path = candidate
        break

if not python_path:
    python_path = "python"

print("Starting Backend server.py using Python:", python_path)
env = os.environ.copy()
env["PYTHONIOENCODING"] = "utf-8"
env["PYTHONUTF8"] = "1"
backend_proc = subprocess.Popen([python_path, "server.py"], cwd=backend_path, env=env)

print("Starting Frontend (React)...")
# On Windows, use shell=True to locate npm automatically
frontend_proc = subprocess.Popen("npm run dev", cwd=frontend_path, shell=True)

print("GUI started! Press Ctrl+C to stop both servers.")

try:
    backend_proc.wait()
    frontend_proc.wait()
except KeyboardInterrupt:
    print("\nShutting down servers...")
    backend_proc.terminate()
    frontend_proc.terminate()

