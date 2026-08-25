import subprocess
import atexit
import time
import webbrowser

def main():
    print('open ssh tunnel to mongo express')
    ssh_process = open_tunnel()
    print('open browser')
    webbrowser.open('http://localhost:8081')
    input('to close tunnel press any key...')
    close_tunnel(ssh_process)

def open_tunnel():
    ssh_process = subprocess.Popen(
        ['ssh', '-L', '8081:localhost:8081', 'myfirstvps', '-N'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    atexit.register(lambda: ssh_process.terminate())
    time.sleep(2)
    return ssh_process

def close_tunnel(ssh_process):
    ssh_process.terminate()
    ssh_process.wait(timeout=5)

if __name__ == '__main__':
    main()