from flask import Flask, render_template, request, jsonify
import re
from num2words import num2words

app = Flask(__name__)

# Saatavilla olevat kielet
KIELET = ["ruotsi", "englanti", "espanja"]

def numbers_to_words(text, lang="fi"):
    """
    Muuntaa kaikki numerot tekstissä sanoiksi.
    Esim. 'Minulla on 3 koiraa' -> 'Minulla on kolme koiraa'
    """
    return re.sub(r'\d+', lambda m: num2words(int(m.group()), lang=lang), text)

def fake_translate(text, source, target):
    """
    Tämä on DEMO-käännös.
    Oikeassa versiossa tähän tulisi OpenAI / LLM -kutsu.
    """
    return f"[{source} → {target}] {text}"

@app.route("/", methods=["GET", "POST"])
def index():
    kaannos = ""

    if request.method == "POST":
        kieli = request.form.get("kieli")
        teksti = request.form.get("teksti")

        # Numerot sanoiksi (suomeksi)
        teksti = numbers_to_words(teksti, lang="fi")

        # Käännös (demo)
        kaannos = fake_translate(teksti, "suomi", kieli)

    return render_template(
        "index.html",
        kielet=KIELET,
        kaannos=kaannos
    )

# AI-tekstin parannus (DEMO, ilman oikeaa API-avainta)
@app.route("/ai-improve", methods=["POST"])
def ai_improve():
    data = request.get_json()
    text = data.get("text", "")

    improved = (
        "Parannettu teksti:\n\n"
        + text.capitalize()
        + "\n\n(Tässä kohtaa oikea tekoäly parantaisi tyyliä ja kielioppia.)"
    )

    return jsonify({"improved": improved})

if __name__ == "__main__":
    app.run(debug=True)
