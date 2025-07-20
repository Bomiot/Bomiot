import subprocess
import socket

def kill_process_on_port(port: int):
    def is_port_in_use(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
    
    def kill_process(port):
        try:
            result = subprocess.run(
                f'netstat -ano | findstr :{port}',
                shell=True, capture_output=True, text=True
            )
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if f':{port}' in line:
                        parts = line.split()
                        if len(parts) >= 5:
                            pid = parts[-1]
                            if pid != 0:
                                subprocess.run(f'taskkill /PID {pid} /F', shell=True)
        except Exception as e:
            print(f"Error: {e}")
    
    if is_port_in_use(port):
        kill_process(port)