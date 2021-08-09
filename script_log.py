
#coding:utf-8
import mysql.connector
from datetime import datetime
import os
import sys


#connecter à la base
conn = mysql.connector.connect(user=os.environ.get("ITEAMS_DB_USER"), password=os.environ.get("ITEAMS_DB_PASSWORD"),
                              host='localhost',database='ITEAMS')
cursor = conn.cursor()


#ouvrir les fichhiers et les (spliter)
file = open(sys.argv[1],"r")
for ligne in file:
	liste = ligne.split(' ')


	#pétites modifications des certaines valeurs
	liste_3 = liste[3]
	liste_3vrai = liste_3.replace('[','')


	liste_7 = liste[7]
	liste_7vrai = liste_7.replace('\\n','')
	Protocole = liste_7vrai.replace('"','')


	UserAgent = None

	try:
		if '"-"' not in liste[11]: UserAgent = ' '.join(liste[11:])
	except:
		pass
		
	
	#Ré-Mis en liste des bonnes valeurs déjà modifiées
	liste_vrai = ['{}'.format(liste[0]),'{}'.format(liste_3vrai),'{}"'.format(liste[5]), \
				'{}'.format(liste[6]),'{}'.format(Protocole),'{}'.format(liste[8])]
	
	
	#formatage des dates dans les fichiers pour correspondre au type DATETIME de la base
	daty = liste_vrai[1]
	daty_split = datetime.strptime(daty, "%d/%b/%Y:%H:%M:%S")
	daty_vrai = datetime.strftime(daty_split, "%Y-%m-%d %H:%M:%S")

	#Condition pour les Code_retour à inserer dans la base
	valeur = liste_vrai[5]
	valeur_vrai = int(valeur) if valeur.isdigit() else None
	
	print(liste_vrai)

	#insertion dans la base
	try:
		cursor.execute(""" INSERT INTO Access_log_server (ip_adress,date_heure,methode,routes,protocole,code_retour,user_agent)
		VALUES (%s,%s,%s,%s,%s,%s,%s)""",(liste_vrai[0],daty_vrai,liste_vrai[2],liste_vrai[3],liste_vrai[4],valeur_vrai,UserAgent))
	except Exception as err:
		print(err)
		continue
	conn.commit()

file.close()
conn.close()
