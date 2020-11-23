from flask import Flask, render_template, redirect, url_for, request, session, escape
from ham import Ham

app = Flask(__name__)
app.secret_key = "hamdiscretekey"

finance = Ham()
finance.secret_key = "financediscretekey"

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/bankAddress', methods=['POST', 'GET'])
def banktoaddress():
    if request.method == "POST":
        country = request.form['country']
        bank = request.form['bank_name']
        acc_no = request.form['acc_no']
        #acc_name = request.form['acc_name']
        session['walletaddress'] = finance.getwallet(f'{country} {acc_no} {bank} {finance.secret_key}', bind='bank')
        #print(session['walletaddress'])

    return render_template('banktoaddress.html')

if __name__ == "__main__":
    app.run()
