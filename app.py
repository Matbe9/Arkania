from flask import Flask, render_template, request, redirect, make_response
import subprocess
import hashlib
import sqlite3

app = Flask(__name__)
app.secret_key = "886f8b70484617eb26264d2b9c95574b20ccbe864571c22d1a993ef8ed492a383afde51fdaf18ba79f899581f0b730d9"
con = sqlite3.connect('./database.db', check_same_thread=False)
cur = con.cursor()

# cur.execute('''CREATE TABLE user (id INTEGER PRIMARY KEY, username text, adresse_email text, password text, id_cookie text)''') #création de la table pour les utilisateur.
# cur.execute('''INSERT INTO user(username, adresse_email, password) VALUES ("matbe", "degueurce.mathieu@gmail.com", "e9cac7f23c0ff27bb3a4e6e7a4662c01")''')
print(cur.execute('''SELECT * FROM user''').fetchall())


def hash_perso(passwordtohash):
    passww = passwordtohash.encode()
    passw2 = hashlib.md5(passww).hexdigest()
    passww2 = passw2.encode()
    passw3 = hashlib.sha256(passww2).hexdigest()
    passww3 = passw3.encode()
    passw4 = hashlib.sha512(passww3).hexdigest()
    passww4 = passw4.encode()
    passwfinal = hashlib.md5(passww4).hexdigest()
    return passwfinal


# d259a3dfbd71ec6c5c118abfee72de33 = permission admin


@app.route('/')
def home():  # put application's code here
    if request.cookies.get('login') == "True":
        return render_template("index.html")
    else:
        return render_template("login.html")


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.method == 'POST':
        user = request.form['nm']
        passw = request.form['pw']
        if passw == "" or user == "":
            return "Merci de remplir tout les champs"

        password = hash_perso(passw)
        patate = cur.execute("""SELECT password FROM user WHERE username=?""", [user])
        if str(patate.fetchall()) == [(f'{password}',)]:
            print("Error!")
        else:
            print('Error')

        resp = make_response(redirect("/"))
        resp.set_cookie("username", user)
        resp.set_cookie("login", "True")
        resp.set_cookie("permission", "d259a3dfbd71ec6c5c118abfee72de33")
        return resp
    else:
        return "ERROR"


@app.route("/logout")
def logout():
    resp = make_response(redirect("/"))
    resp.delete_cookie("login")
    resp.delete_cookie("permission")
    resp.delete_cookie("username")
    return resp


@app.route("/admin/add_user")
def add_user_page():
    if request.cookies.get("login") != "True":
        return redirect("/")

    return render_template("admin/adduser.html")


@app.route("/admin/add_user_exec", methods=['POST'])
def add_user_exec():
    if request.cookies.get("login") == "True":
        if request.method == 'POST':
            user = request.form['nm']
            passw = request.form['pw']
            permi = request.form['pm']

            print(passw)
            #passw = hash_perso(passw)
            # ici création de l'utilisateur avec l'input user
            return "Value:  "+user+" "+passw+" "+permi+"  "
        else:
            return 'Value: '

    elif request.cookies.get("login") != "True":
        return redirect("/")


if __name__ == '__main__':
    app.run()
