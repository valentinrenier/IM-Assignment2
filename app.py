import requests

from flask import Flask, request, jsonify
from flask_cors import CORS
from api import list_user_repos, list_organizations, greet
from gtts import gTTS
import os
import pygame

app = Flask(__name__)
CORS(app)

def get_intent_from_text(text):
    rasa_ip = 'localhost'
    rasa_url = f"http://{rasa_ip}:5005/model/parse"  # URL de l'API de Rasa
    payload = {"text": text}
    intent_functions={"greet":greet,
                        "list_user_repos":list_user_repos, 
                        'list_organizations':list_organizations}
    try :
        response = requests.post(rasa_url, json=payload)
        if response.status_code == 200:
            intent = response.json().get("intent", {}).get("name")
            confidence = response.json().get("intent", {}).get("confidence")
            print(f"Intent détecté : {intent} (confiance : {confidence})")
            function_to_call = intent_functions.get(intent)

            # Appeler la fonction si elle existe
            if function_to_call:
                result = function_to_call()  # Appel de la fonction
                tts = gTTS(text=result, lang='fr')

                # Sauvegarder le fichier audio
                
                tts.save("message.mp3")
                # Initialiser pygame mixer
                pygame.mixer.init()

                # Charger et jouer le fichier audio
                pygame.mixer.music.load("message.mp3")
                pygame.mixer.music.play()
            else:
                print("Intent non pris en charge.")
            return intent
        else:
            print("Erreur lors de la connexion à l'API Rasa")
            return None
    except Exception as e :
        print(e)


# Définissez une route pour écouter sur le port 5000 et récupérer le texte envoyé via POST
@app.route('/receive_text', methods=['POST'])
def receive_texte():
    # Récupérer le contenu JSON de la requête
    data = request.get_json()

    # Vérifier si le texte est bien présent dans la requête
    if not data or 'text' not in data:
        return jsonify({"error": "Aucun texte trouvé dans la requête"}), 400

    # Récupérer le texte
    texte_recu = data['text']
    print(f"Texte reçu : {texte_recu}")

    get_intent_from_text(texte_recu)

    return jsonify({"message": "Texte reçu avec succès", "text": texte_recu}), 200

def get_windows_ip():
    try:
        # Ouvrir le fichier /etc/resolv.conf
        with open('/etc/resolv.conf', 'r') as f:
            # Lire toutes les lignes
            lines = f.readlines()

        # Rechercher la ligne qui contient 'nameserver'
        for line in lines:
            if line.startswith('nameserver'):
                # Extraire l'IP de la ligne
                ip_address = line.split()[1]
                return ip_address

        # Si aucune ligne 'nameserver' n'est trouvée
        return None
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier /etc/resolv.conf: {e}")
        return None


if __name__ == '__main__':
    # Lancer le serveur sur le port 5000
    app.run(port=5000, debug=True)