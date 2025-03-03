from flask import Flask, render_template, request
import openai
from markupsafe import Markup
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Vérification de la clé API OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("⚠️ Erreur : Aucune clé API OpenAI détectée. Vérifiez votre fichier .env")
openai.api_key = openai_api_key

app = Flask(__name__)

# Fonction pour générer l'image avec DALL-E
def generate_image(prompt):
    image_response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return image_response['data'][0]['url']

# Page d'accueil
@app.route("/")
def index():
    return render_template("index.html")

# Route pour poser la question à GPT-4 et générer un tutoriel avec images
@app.route("/ask_gpt", methods=["POST"])
def ask_gpt():
    user_question = request.form["question"]

    # Définition du prompt pour GPT-4
    system_prompt = (
        "Tu es un expert en électromagnétisme DIY, électricité et bricolage. "
        "Ce projet a été conçu par **Trhacknon** pour aider les jeunes à fabriquer un électro-aimant ejecteur de clou "
        "avec des matériaux accessibles. En plus des instructions détaillées en HTML, tu dois inclure des suggestions d'images qui peuvent "
        "aider à la compréhension du tutoriel. Les images doivent correspondre aux étapes décrites. Voici comment tu devrais répondre :\n\n"
        "⚠️ **Tu dois répondre en HTML pur, sans échappement de balises**. "
        "Et pour chaque section, tu devras fournir une image pertinente avec une URL vers celle-ci.\n"
        "Utilise les balises `<p>`, `<h1>`, `<h2>`, `<table>`, `<tr>`, `<td>`, `<ul>`, `<li>` et `<strong>` pour structurer ta réponse.\n\n"
        "=== **EXEMPLE DE FORMAT** ===\n\n"
        "<h2>1. Introduction</h2>\n"
        "<p>Ce projet explique comment fabriquer un électro-aimant capable d'éjecter un clou...</p>\n"
        "<p><img src='URL_DE_L_IMAGE_1'></p>\n\n"
        "<h2>2. Matériel nécessaire</h2>\n"
        "<table>\n"
        "<tr><th>Nom</th><th>Où le trouver</th><th>Prix approximatif</th></tr>\n"
        "<tr><td>Fil de cuivre émaillé</td><td>Magasin électronique / récup</td><td>5-10€</td></tr>\n"
        "<tr><td>Clou en acier doux</td><td>Quincaillerie / récup</td><td>1€</td></tr>\n"
        "<tr><td>Alimentation 9V</td><td>Magasin tech / récup</td><td>2-5€</td></tr>\n"
        "</table>\n"
        "<p><img src='URL_DE_L_IMAGE_2'></p>\n\n"
        "<h2>3. Étapes de fabrication</h2>\n"
        "<h3>🛠️ Préparation</h3>\n"
        "<ul>\n"
        "<li>Coupez <strong>50 cm de fil</strong> et enlevez l'isolation aux extrémités.</li>\n"
        "<li>Enroulez <strong>100 tours</strong> autour du tube plastique.</li>\n"
        "</ul>\n"
        "<p><img src='URL_DE_L_IMAGE_3'></p>\n\n"
    )

    # Envoi de la question à GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ]
    )

    # Récupération de la réponse en HTML
    answer_html = response["choices"][0]["message"]["content"]

    # Génération d'images pour chaque étape
    # On génère maintenant les URLs réelles pour chaque image
    image_url_1 = generate_image("Image of an electromagnet in action with a nail being ejected, showing the copper wire and battery.")
    image_url_2 = generate_image("Tools needed for an electromagnet project, including copper wire, battery, and a nail.")
    image_url_3 = generate_image("Step-by-step process of building an electromagnet: wrapping wire around a tube, connecting to a battery.")

    # Remplacer les placeholders dans le HTML généré par les images
    # Assurez-vous d'utiliser les URL réelles obtenues de DALL·E
    answer_html = answer_html.replace("URL_DE_L_IMAGE_1", image_url_1)
    answer_html = answer_html.replace("URL_DE_L_IMAGE_2", image_url_2)
    answer_html = answer_html.replace("URL_DE_L_IMAGE_3", image_url_3)

    # Retourner la réponse dans la page HTML
    return render_template("index.html", response=Markup(answer_html))

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
