#!/bin/bash

# Recuperer la difference entre les deux logs et mettre dans le fichiers access_maj les nouveau logs
diff -u /var/log/nginx/access.log /var/log/nginx/access_last.log | grep '^-[^-]' | sed 's/^-//' > /var/log/nginx/access_maj.log
# Mettre a jour le dernier fichier pris comme reference.
cp /var/log/nginx/access.log /var/log/nginx/access_last.log
