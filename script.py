import asyncio
import subprocess
async def run_bash_script(script):
    try:
        subprocess.run(
            ["chmod", "+x", script],
            check=True
        )
        result = subprocess.run(
            [script],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return e.stderr

if __name__ == "__main__":
    asyncio.run(run_bash_script("my_script.sh"))
