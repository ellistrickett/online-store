from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', store_status='Online')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['name']
        return redirect(url_for('success', name=user))
    return render_template('login.html')

@app.route('/success/<name>')
def success(name):
    return f"Welcome {name} to the Online Store!"

if __name__ == '__main__':
    app.run(debug=True)