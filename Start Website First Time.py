import subprocess, time, os

def run(cmd):
    return subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)

print("Running migrate...")
subprocess.run(["python", "manage.py", "migrate"])

print("Collecting static files...")
subprocess.run(["python", "manage.py", "collectstatic", "--noinput"])

print("Huey worker...")
run(["python", "manage.py", "run_huey"])

print("Running MSSA Training (Run_All.py)...")
run(["python", "API/Utils/Run_All.py"])

print("Tailwind...")
run(["python", "manage.py", "tailwind", "dev"])