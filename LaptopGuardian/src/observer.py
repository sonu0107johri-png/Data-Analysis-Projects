import psutil
import win32gui
import win32process
import time
import keyboard 
import threading 
import csv 
import os
import win32api
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
ACTIVITY_LOG = LOG_DIR / "activity_log.csv"

def observe_running_processes():
    observations = []

    for process in psutil.process_iter(
        ["pid", "name", "exe", "username", "create_time"]
    ):
        try:
            info = process.info

            observations.append({
                "pid": info["pid"],
                "process_name": info["name"],
                "executable_path": info["exe"],
                "username": info["username"],
                "started_at": (
                    datetime.fromtimestamp(info["create_time"]).isoformat()
                    if info["create_time"]
                    else None
                ),                  
            })
        
        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    return observations

def observe_foreground_window():
    try:
        hwnd = win32gui.GetForegroundWindow()

        if not hwnd:
            return None

        window_title = win32gui.GetWindowText(hwnd)

        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        process = psutil.Process(pid)

        return {
            "pid": pid,
            "process_name": process.name(),
            "executable_path": process.exe(),
            "username": process.username(),
            "window_title": window_title,
        }

    except(
        psutil.NoSuchProcess,
        psutil.AccessDenied,
        psutil.ZombieProcess,
    ):

        return None

def observe_visible_windows():
    visible_windows = []

    def collect_window(hwnd, results):
        if not win32gui.IsWindowVisible(hwnd):
            return

        window_title = win32gui.GetWindowText(hwnd).strip()

        if not window_title:
            return

        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)

            results.append(
                {
                    "pid": pid,
                    "process_name": process.name(),
                    "executable_path": process.exe(),
                    "username": process.username(),
                    "window_title": window_title,
                }
            )
        
        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            pass

    win32gui.EnumWindows(collect_window,visible_windows)

    return visible_windows

def save_activity(activity_data, started_at, ended_at):
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    duration = (ended_at - started_at).total_seconds()

    interpretation = interpret_activity(activity_data)

    file_exists = ACTIVITY_LOG.exists()

    with ACTIVITY_LOG.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "process_name",
                "window_title",
                "activity_type",
                "activity_context",
                "started_at",
                "ended_at",
                "duration_seconds",
            ])

        writer.writerow([
            activity_data["process_name"],
            activity_data["window_title"],
            interpretation["activity_type"],
            interpretation["activity_context"],
            started_at.isoformat(),
            ended_at.isoformat(),
            round(duration, 1),
        ])

        print(
            f"SAVED TO CSV: "
            f"{activity_data['process_name']} | "
            f"{activity_data['window_title']}"
        )

def get_executable_metadata(exe_path):
    metadata = {
        "product_name": "Unknown",
        "file_description": "Unknown",
        "company_name": "Unknown",
    }

    if not exe_path or not os.path.exists(exe_path):
        return metadata
    
    try:
        translations = win32api.GetFileVersionInfo(
            exe_path,
            r"\VarFileInfo\Translation"
        )

        if not translations:
            return metadata
        
        language, codepage = translations[0]
        translation = f"{language:04X}{codepage:04X}"

        fields = {
            "product_name": "ProductName",
            "file_description": "FileDescription",
            "company_name": "CompanyName",
        }

        for key, field in fields.items():
            try:
                value = win32api.GetFileVersionInfo(
                    exe_path,
                    rf"\StringFileInfo\{translation}\{field}"
                )

                if value:
                    metadata[key] = value

            except Exception:
                 pass

    except Exception:
        pass

    return metadata

def build_activity_signals(
  process_name,
  window_title,
  product_name,
  file_description,
  company_name,      
):
    return{
        "process_name": (process_name or "").lower(),
        "window_title": (window_title or "").lower(),
        "product_name": (product_name or "").lower(),
        "file_description": (file_description or "").lower(),
        "company_name": (company_name or "").lower(),
    }

def classify_activity_from_metadata(
    process_name,
    window_title,
    product_name,
    file_description,
    company_name,
):
    
    signals = build_activity_signals(
        process_name,
        window_title,
        product_name,
        file_description,
        company_name,
    )

    process_signal = signals["process_name"]
    title_signal = signals["window_title"]
    product_signal = signals["product_name"]
    description_signal = signals["file_description"]
    company_signal = signals["company_name"]

    scores = {
        "programming": 0,
        "engineering": 0,
        "web_browsing": 0,
        "terminal_activity": 0,
        "file_management": 0,
        "creative_design": 0,
        "gaming": 0,
    }

    if "visual studio" in product_signal or "code editor" in description_signal:
        scores["programming"]+=3

    if "engineering" in description_signal or "simulation" in description_signal:
        scores["engineering"]+=3

    if "browser" in description_signal:
        scores["web_browsing"]+=3

    if "terminal" in description_signal or "console" in description_signal:
        scores["terminal_activity"]+=3

    if "file explorer" in description_signal:
        scores["file_management"]+=3

    if "graphics" in description_signal or "3d" in description_signal:
        scores["creative_design"]+=3

    if "game" in description_signal or "gaming" in description_signal:
        scores["gaming"]+=3

    if "visual studio" in product_signal or "developer" in product_signal:
        scores["programming"]+=2

    if "ansys" in product_signal or "solid edge" in product_signal:
        scores["engineering"]+=2

    if "chrome" in product_signal or "firefox" in product_signal or "microsoft edge" in product_signal:
        scores["web_browsing"]+=2

    if "powershell" in product_signal or "terminal" in product_signal:
        scores["terminal_activity"]+=2

    if "explorer" in product_signal:
        scores["file_managment"]+=2

    if "blender" in product_signal or "krita" in product_signal:
        scores["creative_design"]+=2

    if "game" in product_signal:
        scores["gaming"]+=2

    combined_text = " ".join([
        process_name or "",
        window_title or "",
        product_name or "",
        file_description or "",
        company_name or ""
    ]).lower()

    if any(word in combined_text for word in [
        "visual studio",
        "code editor",
        "developer", 
        "development environment",
        "programming",
        "ide",
    ]):
        return "programming"
    
    if any(word in combined_text for word in [
        "cad",
        "cae",
        "simulation", 
        "engineering",
        "ansys",
        "solid edge",
        "solidworks",
    ]):
        return "engineering"
     
    if any(word in combined_text for word in [
        "browser",
        "chrome",
        "firefox", 
        "microsoft edge",
        "web",
    ]):
        return "web_browsing"
    
    if any(word in combined_text for word in [
        "terminal",
        "powershell",
        "command prompt", 
        "console",
        "shell",
    ]):
        return "terminal_activity"
    
    if any(word in combined_text for word in [
        "file explorer",
        "file manager",
        "windows explorer", 
    ]):
        return "file_management"
    
    if any(word in combined_text for word in [
        "photoshop",
        "illustrator",
        "blender", 
        "graphics",
        "3D",
        "image editing",
    ]):
        return "creative_design"
    
    if any(word in combined_text for word in[
        "gaming",
        "game",
        "citra",
        "pokemon",
        "pokemon",
        "cities: skylines",
        "transport",
        "warfare",
        "palworld",
        "gta",
    ]):
        return "gaming"
    
    return "general"

def interpret_activity(activity_data):
    process_name = activity_data.get("process_name", "").lower()
    window_title = activity_data.get("window_title", "")
    exe_path = activity_data.get("executable_path", "")

    metadata = get_executable_metadata(exe_path)

    product_name = metadata.get("product_name", "Unknown")
    file_description = metadata.get("file_description", "Unknown")
    company_name = metadata.get("company_name", "Unknown")

    activity_type = classify_activity_from_metadata(
        process_name,
        window_title,
        product_name,
        file_description,
        company_name,
    )

    if "code.exe" in process_name:
        activity_type = "programming"

    elif "chrome.exe" in process_name:
        activity_type = "web_browsing"

    elif "citra" in process_name:
        activity_type = "gaming"

    elif "explorer.exe" in process_name:
        activity_type = "file_management"

    elif "powershell.exe" in process_name:
        activity_type = "terminal_activity"

    if product_name != "Unknown":
        activity_context = product_name

    elif file_description != "Unknown":
        activity_context = file_description

    elif window_title:
        activity_context = window_title

    else:
        activity_context = activity_data.get("process_name", "")

    return {
        "activity_type": activity_type,
        "activity_context": activity_context,
        "product_name": product_name,
        "file_description": file_description,
        "company_name": company_name,
    }

def monitor_foreground_changes(interval=1):
    previous_window = None
    previous_data = None
    activity_start = None

    stop_event = threading.Event()

    hotkey = keyboard.add_hotkey(
        "alt+f",
        stop_event.set
    )

    print("\nForeground monitoring started.")
    print("Switch between applications.")
    print("Press Alt+F to stop Guardian Monitoring.\n")

    try:
        while not stop_event.is_set():
            current_window = observe_foreground_window()

            if current_window:
                current_identity = (
                    current_window["pid"],
                    current_window["window_title"]
                )

                current_time = datetime.now()

                if current_identity != previous_window:

                    #Finish Previous Activity
                    if previous_data is not None and activity_start is not None:
                        duration = current_time - activity_start
                        interpretation = interpret_activity(previous_data)

                        print("\nACTIVITY ENDED")
                        print(f"Process: {previous_data['process_name']}")
                        print(f"Window: {previous_data['window_title']}")
                        print(
                            f"Started: "
                            f"{activity_start.strftime('%Y-%m-%d %H:%M:%S')}"
                        )
                        print(
                            f"Ended:"
                            f"{current_time.strftime('%Y-%m-%d %H:%M:%S')}"
                        )

                        print(
                            f"Duration: ",
                            f"{duration.total_seconds():.1f} seconds"
                        )

                        print(f"Activity Type: {interpretation['activity_type']}")

                        print(f"Activity Context: {interpretation['activity_context']}")

                        save_activity(
                            previous_data,
                            activity_start,
                            current_time,
                        )

                    #Start New Activity
                    print("\nACTIVITY STARTED")
                    print(f"Process: {current_window['process_name']}")
                    print(f"Window: {current_window['window_title']}")
                    print(
                        f"Started: "
                        f"{current_time.strftime('%Y-%m-%d %H:%M:%S')}"
                    )

                    previous_window = current_identity
                    previous_data = current_window
                    activity_start = current_time

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nGuardian stopped through termional interrupt.")

    finally:
        #Close the final activity.
        if previous_data is not None and activity_start is not None:
            end_time = datetime.now()
            duration = end_time - activity_start

            print("\nFINAL ACTIVITY ENDED")
            print(f"Process: {previous_data['process_name']}")
            print(f"Window: {previous_data['window_title']}")
            print(
                f"Started:"
                f"{activity_start.strftime('%Y-%m-%d %H:%M:%S')}"
            ) 
            print(
                f"Ended:"
                f"{end_time.strftime('%Y-%m-%d %H:%M:%S')}"
            )

            print(
                f"Duration: "
                f"{duration.total_seconds():.1f} seconds"
            )

            save_activity(
                previous_data,
                activity_start,
                end_time, 
            )

        keyboard.remove_hotkey(hotkey)  

        print("\nGuardian monitoring stopped.")

test_path = r"C:\Windows\explorer.exe"

print("\nEXECUTABLE METADATA TEST")
print(get_executable_metadata(test_path))

if __name__ == "__main__":
    monitor_foreground_changes()