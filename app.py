from flask import Flask, render_template, request
import openai
from markupsafe import Markup
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Vérification de la clé API
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("⚠️ Erreur : Aucune clé API OpenAI détectée. Vérifiez votre fichier .env")
openai.api_key = openai_api_key

app = Flask(__name__)

# Fonction pour générer des images avec DALL-E
def generate_image(description):
    # Exemple avec l'API DALL-E pour générer une image
    response = openai.Image.create(
        prompt=description,
        n=1,
        size="1024x1024"
    )
    # Récupération de l'URL de l'image générée
    image_url = response['data'][0]['url']
    return image_url

# Page d'accueil
@app.route("/")
def index():
    return render_template("index.html")

# Route pour poser la question à GPT-4
@app.route("/ask_gpt", methods=["POST"])
def ask_gpt():
    user_question = request.form["question"]

    # Définition du prompt pour GPT-4
    system_prompt = (
        "Tu es un expert en électromagnétisme DIY, électricité et bricolage. "
        "Ce projet a été conçu par **Trhacknon** pour aider les jeunes à fabriquer un électro-aimant ejecteur de clou "
        "avec des matériaux accessibles.\n\n"
        "⚠️ **Tu dois répondre en HTML pur, sans échappement de balises**.\n"
        "Utilise les balises `<p>`, `<h1>`, `<h2>`, `<table>`, `<tr>`, `<td>`, `<ul>`, `<li>` et `<strong>` pour structurer ta réponse.\n\n"
        "=== **EXEMPLE DE FORMAT** ===\n\n"
        "<h2>1. Introduction</h2>\n"
        "<p>Ce projet explique comment fabriquer un électro-aimant capable d'éjecter un clou...</p>\n\n"
        "<h2>2. Matériel nécessaire</h2>\n"
        "<table>\n"
        "<tr><th>Nom</th><th>Où le trouver</th><th>Prix approximatif</th></tr>\n"
        "<tr><td>Fil de cuivre émaillé</td><td>Magasin électronique / récup</td><td>5-10€</td></tr>\n"
        "<tr><td>Clou en acier doux</td><td>Quincaillerie / récup</td><td>1€</td></tr>\n"
        "<tr><td>Alimentation 9V</td><td>Magasin tech / récup</td><td>2-5€</td></tr>\n"
        "</table>\n\n"
        "<h2>3. Étapes de fabrication</h2>\n"
        "<h3>🛠️ Préparation</h3>\n"
        "<ul>\n"
        "<li>Coupez <strong>50 cm de fil</strong> et enlevez l'isolation aux extrémités.</li>\n"
        "<li>Enroulez <strong>100 tours</strong> autour du tube plastique.</li>\n"
        "</ul>\n\n"
        "<h3>⚙️ Branchement</h3>\n"
        "<ul>\n"
        "<li>Connectez un fil à l'interrupteur et l'autre à la batterie.</li>\n"
        "<li>Placez le clou au centre et activez l'interrupteur.</li>\n"
        "</ul>\n\n"
        "<h3>✨ Opération</h3>\n"
        "<ul>\n"
        "<li>Activez l'interrupteur pour générer le champ électromagnétique qui éjecte le clou.</li>\n"
        "</ul>\n\n"
        "<h2>4. Conseils et astuces</h2>\n"
        "<ul>\n"
        "<li>Plus de <strong>tours</strong> = plus de puissance.</li>\n"
        "<li>Expérimente avec <strong>différentes tensions (5V, 9V, 12V)</strong> pour varier la puissance.</li>\n"
        "</ul>\n\n"
        "<h2>5. Avertissements de sécurité</h2>\n"
        "<ul>\n"
        "<li>⚠️ <strong>Ne pas dépasser 12V</strong> pour éviter la surchauffe.</li>\n"
        "<li><strong>Ne jamais toucher les fils dénudés</strong> sous tension.</li>\n"
        "</ul>\n\n"
        "<h2>6. Mention Trhacknon</h2>\n"
        "<p>Ce projet est développé par <strong>Trhacknon</strong> pour la communauté DIY et hacker.</p>\n"
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

    # Générer une image pour accompagner le tutoriel
    image_description = """
    "An electro-magnetism DIY project in action, illustrating a copper coil with a steel nail at the center. The coil is powered by a 9V battery, and when current passes through the copper wire, the nail is ejected due to the magnetic field. The image shows a close-up of the copper coil tightly wound around a plastic tube, with clear visibility of the shiny copper wire. The battery is visible and connected with wires. Sparks are emitted from the connections to show the electricity flow. The steel nail is visibly being pushed away from the coil, demonstrating the ejection force. The image should have a sense of motion with a blurred nail to emphasize the rapid action. The setting is a minimalistic DIY workshop, with tools and materials like a soldering iron, pliers, and a workbench in the background. The focus should be on the interaction between the electricity, the copper coil, and the nail, with a technical yet hands-on DIY atmosphere."
    """
    image_url = generate_image(image_description)

    # Ajouter l'image dans le contenu HTML
    image_html = f'<img src="{image_url}" alt="Schéma du montage électro-aimant" style="width:100%; max-width:600px; margin:20px 0;">'
    answer_html += image_html

    # Retourner la réponse dans la page HTML
    return render_template("index.html", response=Markup(answer_html))

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
