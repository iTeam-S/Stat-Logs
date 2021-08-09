from flask import Flask, jsonify, request, render_template, url_for
import mysql.connector
from model import Model
from datetime import datetime
import calendar

Database = Model()
app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET', 'POST'])
def login():
    if list(request.form) != []:
        user_log = request.form.get("login")
        pass_log = request.form.get("password")
        error_login = """
            Email et Mot de passe incorrect!!! Veuillez saisir à nouveau"
        """

        # fetch the user_email and password in BDD:
        login = Database.login(user_log, pass_log)
        if (list(login) != []):
            return main(user_log)
        else:
            return render_template("index.html", error_login=error_login)

    else:
        return render_template("index.html")


@app.route('/statistiques', methods=['GET', 'POST'])
def main(user_log=None):
    # GENERAL STATISTICS MANAGEMENT:
    # get the values in HTML:
    if user_log or request.form.get('user_log'):
        if request.form.get('daty') != None:
            user_log = request.form.get('user_log')
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

        # fetch the data in BDD:
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

        # MANAGEMENT OF THE MAXIMUM:
        resultat_max = Database.max_visiteur(date)
        h_max = 0
        n_max = 0
        for v_max in resultat_max:
            h_max = int(v_max[0])
            n_max = v_max[1]

        # MANAGEMENT OF THE MINIMUM:
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
            n_min=n_min, daty_vis=daty_vis, user_log=user_log
        )
    else:
        return login()


# Route for static files:
@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)


app.run()
