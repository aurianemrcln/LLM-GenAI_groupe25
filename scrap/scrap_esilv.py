import requests
from bs4 import BeautifulSoup
import re

# 1. Récupérer le contenu de la page
url = "https://www.esilv.fr/admissions/concours-avenir/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 2. Extraire la div "content_wrapper"
content_wrapper = soup.find("div", id="content_wrapper")
contenu = content_wrapper.get_text(separator='\n', strip=True)

# 3. Nettoyer les retours à la ligne avant les minuscules
lignes = contenu.split('\n')
lignes_nettoyees = []
for i, ligne in enumerate(lignes):  # supprime le retour à la ligne quand c'est un minuscule avant ou quand c'est 'Paris' ou 'Concours' ou une ponctuation
    if i > 0 and len(ligne) > 0 and (ligne[0].islower() or ligne in ['Paris', 'Concours', 'AVENIR', 'Parcoursup', 'Bac', 'Classement'] or re.match(r'^[.,;:!?]', ligne)):
        lignes_nettoyees[-1] += ' ' + ligne
    else:
        lignes_nettoyees.append(ligne)
contenu_nettoye = '\n'.join(lignes_nettoyees)

# 4. Extraire la première ligne pour le nom du fichier
premiere_ligne = lignes_nettoyees[0] if lignes_nettoyees else "contenu_site"
nom_fichier = re.sub(r'[^\w\-_]', '_', premiere_ligne.strip()) + ".txt"

# 5. Sauvegarder dans un fichier texte
with open(f"scrap/{nom_fichier}", "w", encoding="utf-8") as fichier:
    fichier.write(contenu_nettoye)

print(f"Fichier sauvegardé sous : scrap/{nom_fichier}")