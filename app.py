from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
import evaluate

app = Flask(__name__)
app.secret_key = b'abcde'
admin = '12345'

users_names = {int(l.split(',')[1][:-1]): l.split(',')[0] for l in open('users.csv').readlines()[1:]}
submissions = {}

@app.route('/')
def home():
    if 'nmec' not in session:
        return redirect(url_for('login'))
    code = submissions.get(session['nmec'], '')
    return render_template('dashboard.html', code=code, users_names=users_names)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            nmec = int(request.form['nmec'])
        except:
            nmec = None
        if nmec not in users_names:
            flash(f'Unauthorized access for {nmec}')
            return redirect(url_for('login'))
        session['nmec'] = nmec
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/submit-code', methods=['POST'])
def submit_my_code():
    code = request.form['code']
    submissions[session['nmec']] = code
    compile_code, compile_output = evaluate.compile(code)
    compile_output = compile_output.replace('\n', '<br>')
    if compile_code == 0:
        program_output = evaluate.test(request.form['stdin']).replace('\n', '<br>')
    else:
        program_output = ''
    return {'compile_code': compile_code, 'compile_output': compile_output,
        'program_output': program_output}

@app.route('/clear-submissions')
def clear_submissions():
    print('clear submissions')
    global submissions
    submissions = {}
    return 'OK'

@app.route('/get-submissions')
def get_others_codes():
    ret = [{'code': submissions[s], 'name': users_names[s]} for s in submissions]
    return jsonify(ret)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
