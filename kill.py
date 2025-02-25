# import psutil

# def kill_process_by_name(process_name):
#     """Terminate a process by its name."""
#     for process in psutil.process_iter(attrs=['pid', 'name']):
#         if process.info['name'] == process_name:
#             print(f"Terminating process: {process.info['name']} (PID: {process.info['pid']})")
#             psutil.Process(process.info['pid']).terminate()
#             return True
#     print(f"No process named '{process_name}' found.")
#     return False

# # Example: Kill Notepad on Windows or a process like "python3" on Linux
# kill_process_by_name(input("Enter Process name : "))  # Windows
# # kill_process_by_name("python3")  # Linux

# import psutil

# def kill_process_by_pid(pid):
#     """Terminate a process using its PID."""
#     try:
#         process = psutil.Process(pid)
#         print(f"Terminating process: {process.name()} (PID: {pid})")
#         process.terminate()  # Graceful termination
#         return True
#     except psutil.NoSuchProcess:
#         print(f"No process found with PID: {pid}")
#     except psutil.AccessDenied:
#         print(f"Access denied! Try running with sudo/admin privileges.")
#     return False

# # Example usage
# kill_process_by_pid(int(input("Enter PID : ")))  # Replace 1234 with the actual PID

import psutil

def kill_process(target):
    """Terminate a process by name or PID."""
    if target.isdigit():  # If input is a number, treat it as a PID
        pid = int(target)
        try:
            process = psutil.Process(pid)
            process.terminate()
            print(f"Terminated process: {process.name()} (PID: {pid})")
        except psutil.NoSuchProcess:
            print(f"No process found with PID: {pid}")
        except psutil.AccessDenied:
            print(f"Access denied! Try running with sudo/admin privileges.")
    else:  # Otherwise, treat it as a process name
        found = False
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if process.info['name'].lower() == target.lower():
                try:
                    psutil.Process(process.info['pid']).terminate()
                    print(f"Terminated process: {process.info['name']} (PID: {process.info['pid']})")
                    found = True
                except psutil.NoSuchProcess:
                    print(f"No process found with PID: {pid}")
                except psutil.AccessDenied:
                    print(f"Access denied! Try running with sudo/admin privileges.")
        if not found:
            print(f"No process named '{target}' found.")

# Example usage
target_input = input("Enter process name or PID: ").strip()
kill_process(target_input)

