import os
import sqlite3
import hashlib

mdp1 = ""
mdp2 = ""
conf1 = False

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

if os.system("groups") != "root":
    exit("L'installation doit être fait en root!")

print("Bienvenue dans l'installation d'Arkania!")

os.system("git clone https://github.com/Matbe9/Arkania.git")
os.system('touch ./Arkania/database.db')
con = sqlite3.connect('./Arkania/database.db', check_same_thread=False)
cur = con.cursor()
cur.execute('''CREATE TABLE user (id INTEGER PRIMARY KEY, username text, adresse_email text, password text, id_cookie text, permission text)''') #création de la table pour les utilisateur.
cur.execute('''CREATE TABLE server (id INTEGER PRIMARY KEY, name text, owner_adresse_email text, user_permission text)''') #création de la table pour les serveurs.
cur.execute('''CREATE TABLE permission (id INTEGER PRIMARY KEY, name text, allowed_to text)''') #création de la table pour les permissions.

print("---------------------------------------------------------------------------------------------------------------")
while not conf1:
    print("Nous allons donc créer un premier compte administrateur.")
    username = input("    Nom d'utilisateur: ")
    email = input("    Adresse e-mail: ")

    mdp1 = input("    Mot de passe: ")
    mdp2 = input("    Confirmation du mot de passe: ")
    confirm = input("Confirmez vous les données ci-dessus? ")
    if confirm == "yes" or confirm == "oui" or confirm == "y" or confirm == "o":
        conf1 = True
        cur.execute(f'''INSERT INTO user(username, adresse_email, password, permission) VALUES ("{username}", "{email}", "{hash_perso(mdp2)}", "d259a3dfbd71ec6c5c118abfee72de33")''')
print("---------------------------------------------------------------------------------------------------------------")

launch_startup = input("Voullez vous lancez Arkania au lancement de votre serveur?")
if launch_startup == "yes" or launch_startup == "oui" or launch_startup == "y" or launch_startup == "o":
    os.system("touch /etc/systemd/system/arkania.service")
    os.system(f"""[Unit]
Description=Arkania server Utilities

[Service]
ExecStart=/usr/bin/python3 {os.getcwd()}/Arkania/app.py

[Install]
WantedBy=multi-user.target""")
    os.system("systemctl enable arkania")

print("---------------------------------------------------------------------------------------------------------------")

print("Nous venons de finir l'instalation d'Arkania! Vous pouvez maintenant sur https://127.0.0.1:5000/  pour pouvoir continuer l'installation d'Arkania")