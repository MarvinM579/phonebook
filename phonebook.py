from flask import Flask, render_template, request, redirect, session, url_for
import pg

db = pg.DB(host="localhost", user="postgres", passwd="rocket", dbname="phonebook")

app = Flask('phone book')


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")


@app.route('/submit_login', methods=['POST', 'GET'])
def submit_login():
    username = request.form.get('username')
    password = request.form.get('password')
    query = db.query("select * from users where username = '%s'" % username)
    result_list = query.namedresult()
    if len(result_list) > 0:
        user = result_list[0]
        if user.password == password:
            session['name'] = user.name
            return redirect('/contacts')
        else:
            return redirect('/login')
    else:
        return redirect('/login')


@app.route('/logout_page')
def logout_page():
    return "<h1>Goodbye!</h1>"


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    del session['name']
    return redirect('/')


@app.route('/contacts')
def contacts():
    contacts = db.query('select * from phonebook').namedresult()
    return render_template(
        'contacts.html',
        title='All Contacts',
        contacts=contacts
    )


@app.route('/new_contact')
def new_contact():
    return render_template(
        'new_contact.html',
        title='New Contact'
    )


@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')
    db.insert('phonebook',
              name=name,
              phone_number=phone_number,
              email=email)
    return redirect('/contacts')


@app.route('/update_contact')
def update_contact():
    id = int(request.args.get('id'))
    query = db.query('''
    select * from phonebook
    where id = %d''' % id)
    contact = query.namedresult()[0]
    return render_template(
        'update_contact.html',
        contact=contact
    )


@app.route('/submit_update', methods=['POST'])
def submit_update():
    id = int(request.form.get('id'))
    name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')
    action = request.form.get('action')
    if action == 'update':
        db.update('phonebook', {
            'id': id,
            'name': name,
            'phone_number': phone_number,
            'email': email
        })
    elif action == 'delete':
        db.delete('phonebook', {'id': id})
    else:
        raise Exception("ERROR")
    return redirect('/contacts')
app.secret_key = 'cn0hn42'

if __name__ == '__main__':
    app.run(debug=True)
