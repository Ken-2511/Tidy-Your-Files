import subprocess

result = subprocess.run(["ls"], cwd="/", capture_output=True, text=True)

print(result.stdout)
