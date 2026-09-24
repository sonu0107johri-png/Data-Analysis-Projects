import psutil
from observer import get_executable_metadata

print("\n AUTOMATIC APPLICATION METADATA TEST\n")

for process in psutil.process_iter(["pid", "name", "exe"]):
    try:
        info = process.info
        exe_path = info["exe"]

        if not exe_path:
            continue

        metadata = get_executable_metadata(exe_path)

        print(f"Process: {info['name']}")
        print(f"Executable: {exe_path}")
        print(f"Product: {metadata['product_name']}")
        print(f"Description: {metadata['file_description']}")
        print(f"Company: {metadata['company_name']}")
        print("-"*60)
        
    except(
        psutil.NoSuchProcess,
        psutil.AccessDenied,
        psutil.ZombieProcess
    ):
        continue
        