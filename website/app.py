from flask import Flask, jsonify, request, render_template, url_for, send_from_directory
import mysql.connector
from model import Model
from datetime import datetime
import calendar

Database = Model()
app = Flask(__name__)
app.config["DEBUG"] = True


#route for login and this All conditions:
@app.route('/', methods=['GET', 'POST'])
def login():
    if list(request.form) != []:
        user_log = request.form.get("login")
        pass_log = request.form.get("password")
        error_login = """
            Email et Mot de passe incorrect!!! Veuillez saisir à nouveau"
        """

        # Verify the user_email and password in BDD(if exist or not):
        login = Database.login(user_log, pass_log)
        if (list(login) != []):
            return default_statistique(user_log)
        else:
            return render_template("index.html", error_login=error_login)
    else:
        return render_template("index.html")


#route for the default page of the statistic
@app.route('/default_statistique', methods=['GET', 'POST'])
def default_statistique(user_log=None):
    if user_log or request.form.get('user_log'):
        
        date = datetime.now().strftime("%Y-%m-%d")
        statut = ''
        # fetch the data for default statistique of the date now in BDD:
        resultat_stat1 = Database.statistique(date,statut)
        dico1 = {}
        dico_sort1 = {}
        for row1 in resultat_stat1:
            dico1[int(row1[2])] = int(row1[3])

        for y in range(24):
            if y not in dico1.keys():
                dico1[y] = 0
            dico_sort1[y] = dico1[y]
        liste1 = []
        for valeur1 in dico_sort1.values():
            liste1.append(valeur1)
        return render_template("default_stat_page.html", liste1 = liste1)

    else:
        return login()


#route of the detail of the statistic
@app.route('/statistiques', methods=['GET', 'POST'])
def main():
    # GENERAL STATISTICS MANAGEMENT:
    # get the values in HTML:
    if request.form.get('daty') != None:
        date_get = request.form.get('daty')
        date = datetime.strptime(
            str(date_get), "%Y-%m-%d").strftime("%Y-%m-%d")
        statut = request.form.get('statut')
        daty_vis = datetime.strptime(
            str(date_get), "%Y-%m-%d").strftime("%d %b %Y")
    else:
        date = datetime.now().strftime("%Y-%m-%d")
        statut = 200
        daty_vis = datetime.now().strftime("%d %b %Y")

    # fetch the data in BDD corresponding to the date and  the statut:
    resultat_stat = Database.statistique(date, statut)
    dico = {}
    dico_sort = {}
    for row in resultat_stat:
        dico[int(row[2])] = int(row[3])

    for i in range(24):
        if i not in dico.keys():
            dico[i] = 0
        dico_sort[i] = dico[i]
    liste = []
    for valeur in dico_sort.values():
        liste.append(valeur)

    # MANAGEMENT OF THE VISITOR'S NUMBER:
    # for the maximum:
    resultat_max = Database.max_visiteur(date)
    h_max = 0
    n_max = 0
    for v_max in resultat_max:
        h_max = int(v_max[0])
        n_max = v_max[1]

    # for the muinimum:
    resultat_min = Database.min_visiteur(date)
    h_min = 0
    n_min = 0
    for v_min in resultat_min:
        h_min = int(v_min[0])
        n_min = v_min[1]

    return render_template(
        'stat_wbs_page.html',
        liste=liste, date=date,
        n_max=n_max, h_min=h_min,
        statut=statut, h_max=h_max,
        n_min=n_min, daty_vis=daty_vis
    )
    


# Route for static files:
@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)


app.run()
