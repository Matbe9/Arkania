from flask import Flask, render_template, request, redirect, make_response
from markupsafe import escape
import hashlib
import sqlite3

app = Flask(__name__)
app.secret_key = "886f8b70484617eb26264d2b9c95574b20ccbe864571c22d1a993ef8ed492a383afde51fdaf18ba79f899581f0b730d9"
con = sqlite3.connect('./database.db', check_same_thread=False)
cur = con.cursor()

"""Attention! Ces lignes détruise la base de donné!"""
"""
cur.execute('''DROP TABLE user''')
cur.execute('''DROP TABLE server''')
cur.execute('''CREATE TABLE user (id INTEGER PRIMARY KEY, username text, adresse_email text, password text, id_cookie text, permission text)''') #création de la table pour les utilisateur.
cur.execute('''CREATE TABLE server (id INTEGER PRIMARY KEY, name text, owner_adresse_email text, user_permission text)''') #création de la table pour les serveurs.
cur.execute('''CREATE TABLE permission (id INTEGER PRIMARY KEY, name text, allowed_to text)''') #création de la table pour les permissions.
cur.execute('''INSERT INTO permission(name, allowed_to) VALUES ("admin","all")''')
cur.execute('''INSERT INTO user(username, adresse_email, password, permission) VALUES ("admin", "test2@test.test", "ae077ca98eb2cfe8d4e90b84d43e907b", "d259a3dfbd71ec6c5c118abfee72de33")''')
cur.execute('''INSERT INTO user(username, adresse_email, password, permission) VALUES ("matbe", "degueurce.mathieu@gmail.com", "e9cac7f23c0ff27bb3a4e6e7a4662c01", "d259a3dfbd71ec6c5c118abfee72de33")''')
con.commit()
"""


def hash_perso(passwordtohash):
    passww = passwordtohash.encode()
    passww = hashlib.md5(passww).hexdigest()
    passww = passww.encode()
    passww = hashlib.sha256(passww).hexdigest()
    passww = passww.encode()
    passww = hashlib.sha512(passww).hexdigest()
    passww = passww.encode()
    passww = hashlib.md5(passww).hexdigest()
    return passww

# d259a3dfbd71ec6c5c118abfee72de33 = permission admin


@app.route('/')
def home():  # put application's code here
    if request.cookies.get('login') == "True":
        if request.cookies.get("permission") == "d259a3dfbd71ec6c5c118abfee72de33":
            return redirect("/admin/index")
        return render_template("index.html", cur=cur, str=str)

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    resp = make_response(redirect("/"))
    resp.delete_cookie("login")
    resp.delete_cookie("permission")
    resp.delete_cookie("username")
    return resp


@app.route("/admin/")
def admin():
    if request.cookies.get("login") == "True" and request.cookies.get("permission") == "d259a3dfbd71ec6c5c118abfee72de33":
        return redirect("/admin/index")
    return redirect("/")

@app.route("/admin/index")
def index_admin():
    if request.cookies.get("permission") == "d259a3dfbd71ec6c5c118abfee72de33":
        return render_template("admin/index.html", cur=cur, str=str)


@app.route("/admin/add_user")
def add_user_page():
    if request.cookies.get("login") == "True" and request.cookies.get("permission") == "d259a3dfbd71ec6c5c118abfee72de33":
        return render_template("admin/adduser.html")

    return redirect("/")


@app.route("/admin/show_user/")
@app.route("/admin/show_user/<user>")
def show_user(user=None):
    if request.cookies.get("login") == "True"  and request.cookies.get("permission") == "d259a3dfbd71ec6c5c118abfee72de33":
        return render_template("admin/show_user.html", cur=cur, user=user)

    return redirect("/")


@app.route("/admin/show_server")
def admin_show_server():
    if request.cookies.get("login") == "True" and request.cookies.get("permission") == "d259a3dfbd71ec6c5c118abfee72de33":
        return redirect("/admin/")
        # return render_template("show_server.html", cur=cur)

    return redirect("/")


@app.route("/admin/delete_user")
def delete_user():
    if request.cookies.get("login") == "True" and request.cookies.get("permission") == "d259a3dfbd71ec6c5c118abfee72de33":
        return redirect("/admin/")
        # return render_template("show_server.html", cur=cur)

    return redirect("/")

########################################################################################################################
#                                                    A.P.I                                                             #
########################################################################################################################


@app.route("/api/v1/delete_user/<username_to_delete>")
def delete_user_api(username_to_delete):
    """Cette endpoint est à utiliser avec les valeurs dans l'url."""
    if request.cookies.get("login") == "True" and request.cookies.get("permission") == "d259a3dfbd71ec6c5c118abfee72de33" and username_to_delete is not False:
        cur.execute("DELETE FROM user WHERE username = ?", (escape(username_to_delete),))
        con.commit()
        resp = make_response(redirect("/admin/show_user"))
        # return f"L'utilisateur {username_to_delete} a bien été supprimé!"
        return resp


@app.route("/api/v1/admin/add_server", methods=["POST"])
def add_server():
    if request.cookies.get("login") == "True" and request.cookies.get("permission") == "d259a3dfbd71ec6c5c118abfee72de33":
        if request.method == 'POST':
            user = request.form['nm']
            mail = request.form['em']
            # passw = request.form['pw']
            # permi = request.form['pm']

            # passw = hash_perso(passw)
            # ici création de l'utilisateur avec l'input user
            cur.execute('''INSERT INTO server(name, owner_adresse_email) VALUES (?, ?)''', (user, mail))
            con.commit()
            return "C'est bon"

    return redirect("/")


@app.route('/api/v1/login', methods=['POST'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        passw = request.form['pw']

        if passw == "" or user == "":
            return "Merci de remplir tout les champs"

        password = hash_perso(passw)
        check_user = cur.execute("SELECT * FROM user WHERE username=?", (user,))

        row = check_user.fetchone()

        while row is not None:
            if row[1] != user:
                return "Erreur avec le login"
            else:
                if row[3] == password:
                    perm_allowed = row[5]
                    print(perm_allowed) 

                    resp = make_response(redirect("/"))
                    resp.set_cookie("username", user)
                    resp.set_cookie("login", "True")
                    resp.set_cookie("permission", perm_allowed)
                    return resp
                else:
                    return "Mauvais mot de passe"
        return "Erreur, vous n'êtes pas référencé dans la base de donnée..."
    else:
        return "ERROR"


@app.route("/api/v1/admin/add_user", methods=['POST'])
def add_user_exec():
    if request.cookies.get("login") == "True" and request.cookies.get("permission") == "d259a3dfbd71ec6c5c118abfee72de33":
        if request.method == 'POST':
            user = request.form['nm']
            mail = request.form['em']
            passw = request.form['pw']
            # permi = request.form['pm']

            passw = hash_perso(passw)
            # ici création de l'utilisateur avec l'input user
            cur.execute(f'''INSERT INTO user(username, adresse_email, password, permission) VALUES (?, ?, ?, "d259a3dfbd71ec6c5c118abfee72de33")''', (user, mail, passw))
            con.commit()
            return "C'est bon"
        else:
            return "C'est pas bon"

    return redirect("/")


if __name__ == '__main__':
    app.run()
