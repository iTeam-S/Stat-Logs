import os
import mysql.connector
import os

class Model():
    def __init__(self):
        self.conn = mysql.connector.connect(user=os.environ.get("ITEAMS_DB_USER"),
            password=os.environ.get("ITEAMS_DB_PASSWORD"),
            host='localhost',database='ITEAMS')

        self.cursor = self.conn.cursor()

    # Method fot the statistic generaly:
    def statistique(self, date, statut):
        self.cursor.execute("""
            SELECT id, DATE_FORMAT(date_heure, '%Y-%m-%d') AS DATY,
            DATE_FORMAT(date_heure, '%H') AS ORA,
            COUNT(code_retour) AS Nombre, code_retour
            FROM Access_log_server 
            WHERE code_retour = %s AND DATE_FORMAT(date_heure, '%Y-%m-%d') = %s 
            GROUP BY ora, code_retour 
            ORDER BY daty, ora""", (statut, date))
        result = self.cursor.fetchall()
        return result


    #methods to fetch all data to the dafault_stat_page: 
    def default_statistique(self, date):
        self.cursor.execute("""
            SELECT id, DATE_FORMAT(date_heure, '%Y-%m-%d') AS DATY,
            DATE_FORMAT(date_heure, '%H') AS ORA,
            COUNT(code_retour) AS Nombre
            FROM Access_log_server 
            WHERE DATE_FORMAT(date_heure, '%Y-%m-%d') = %s 
            GROUP BY ora
            ORDER BY daty, ora""", (date, ))   
        result1 = self.cursor.fetchall()
        return result1


    # Method for the maximum number of visitor:
    def max_visiteur(self, date):
        self.cursor.execute(""" SELECT ORA, nombre
                    FROM 
                    (
                        SELECT DATE_FORMAT(date_heure, '%H') AS ORA,
                        COUNT(DISTINCT ip_adress) AS nombre
                        FROM Access_log_server 
                        WHERE DATE_FORMAT(date_heure, '%Y-%m-%d') = %s
                        GROUP BY DATE_FORMAT(date_heure, '%H')
                    )
                    AS tabl 
                    WHERE nombre = (SELECT MAX(nombre)
                    FROM ((
                            SELECT DATE_FORMAT(date_heure, '%H') AS ORA,
                            COUNT(DISTINCT ip_adress) AS nombre
                            FROM Access_log_server 
                            WHERE DATE_FORMAT(date_heure, '%Y-%m-%d') = %s
                            GROUP BY DATE_FORMAT(date_heure, '%H')
                        ) AS tabl)) """, (date, date))
        result_max = self.cursor.fetchall()
        return result_max


    # Method for the minimum number of visitor:
    def min_visiteur(self, date):
        self.cursor.execute(""" SELECT ORA, nombre
                    FROM 
                    (
                        SELECT DATE_FORMAT(date_heure, '%H') AS ORA,
                        COUNT(DISTINCT ip_adress) AS nombre
                        FROM Access_log_server 
                        WHERE DATE_FORMAT(date_heure, '%Y-%m-%d') = %s
                        GROUP BY DATE_FORMAT(date_heure, '%H')
                    )
                    AS tabl 
                    WHERE nombre = (SELECT MIN(nombre)
                    FROM ((
                            SELECT DATE_FORMAT(date_heure, '%H') AS ORA,
                            COUNT(DISTINCT ip_adress) AS nombre
                            FROM Access_log_server 
                            WHERE DATE_FORMAT(date_heure, '%Y-%m-%d') = %s
                            GROUP BY DATE_FORMAT(date_heure, '%H')
                        ) AS tabl)) """, (date, date))
        result_min = self.cursor.fetchall()
        return result_min


    # Method for the management of the user:
    def login(self, user_log, pass_log):
        self.cursor.execute(""" SELECT 1  FROM user_log_server
                    WHERE email = %s and mot_de_passe = %s """, (user_log, pass_log))

        result_user = self.cursor.fetchall()
        return result_user
