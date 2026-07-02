import subprocess
import sys

print("Starting ORBIT-I...")
print("Opening in browser...")

subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])