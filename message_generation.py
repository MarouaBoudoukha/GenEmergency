from flask import Flask, request, jsonify
import os
import openai
from dotenv import load_dotenv

app = Flask(__name__)

# Charger les variables d'environnement
load_dotenv()

# Configuration Azure OpenAI
openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_API_BASE")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# Fonction pour générer le texte d'urgence en fonction du type d'urgence
def generer_texte_urgence(donnees_accident):
    type_urgence = donnees_accident.get("type_urgence", "urgence_generale")
    latitude = donnees_accident.get("latitude", "inconnue")
    longitude = donnees_accident.get("longitude", "inconnue")
    gravite = donnees_accident.get("gravite", "non spécifiée")

    prompts = {
        "accident_de_voiture": (
            f"Un accident de voiture a été détecté aux coordonnées {latitude}, {longitude}. "
            f"La gravité est {gravite}. Génère un message d'urgence clair et concis pour les services de secours."
        ),
        "accident_randonnee": (
            f"Un accident de randonnée a été détecté aux coordonnées {latitude}, {longitude}. "
            f"La gravité est {gravite}. Génère un message d'urgence clair et concis pour les services de secours."
        ),
        "chute_personnes_agees": (
            f"Une chute ou un problème de santé chez une personne âgée a été détecté aux coordonnées {latitude}, {longitude}. "
            f"La gravité est {gravite}. Génère un message d'urgence clair et concis pour les services de secours."
        ),
        "incendie": (
            f"Un incendie a été détecté aux coordonnées {latitude}, {longitude}. "
            f"La gravité est {gravite}. Génère un message d'urgence clair et concis pour les services de secours."
        )
    }

    prompt = prompts.get(type_urgence,
                         f"Une urgence a été détectée aux coordonnées {latitude}, {longitude}. "
                         f"La gravité est {gravite}. Génère un message d'urgence clair et concis pour les services de secours.")

    try:
        response = openai.ChatCompletion.create(
            engine="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates emergency messages based on input data."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.3,
            n=1,
            stop=None
        )
        texte_urgence = response.choices[0].message.content.strip()
        print(f"Texte d'urgence généré : {texte_urgence}")
        return texte_urgence
    except Exception as e:
        print(f"Erreur lors de la génération du texte d'urgence : {e}")
        return None

# Endpoint pour recevoir les données
@app.route('/api/data', methods=['POST'])
def receive_data():
    # Obtenir les données JSON de la requête
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    type_urgence = data.get('type_urgence', 'urgence_generale')
    heart_rate = data.get('heart_rate')
    car_velocity = data.get('car_velocity')
    timestamp = data.get('timestamp', 'inconnu')

    print(f"Type d'urgence: {type_urgence}, Heart rate: {heart_rate}, Car velocity: {car_velocity}, Timestamp: {timestamp}")

    # Détection des conditions d'urgence
    urgence_detectee = False
    if type_urgence == "accident_de_voiture" and (heart_rate < 50 or car_velocity == 0):
        urgence_detectee = True
    elif type_urgence == "accident_randonnee" and (heart_rate < 50):
        urgence_detectee = True
    elif type_urgence == "chute_personnes_agees" and (heart_rate < 50):
        urgence_detectee = True
    elif type_urgence == "incendie" and (car_velocity == 0):
        urgence_detectee = True

    if urgence_detectee:
        print(f"Urgence détectée: {type_urgence}")
        # Générer le message d'urgence
        texte_urgence = generer_texte_urgence(data)
        if texte_urgence:
            # Pour le moment, nous allons simplement retourner le message généré
            # Vous pouvez étendre cette partie pour intégrer d'autres fonctionnalités
            return jsonify({
                "message": "Urgence détectée et message généré.",
                "texte_urgence": texte_urgence
            }), 200

    # Retourner une réponse de succès sans action si aucune urgence n'est détectée
    return jsonify({"message": "Données reçues avec succès, aucune urgence détectée."}), 200

if __name__ == "__main__":
    # Exécute le serveur sur localhost à port 5001
    app.run(host="0.0.0.0", port=5001)
