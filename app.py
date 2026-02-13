from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# ==============================
# CONFIGURACIÓN OPENAI
# ==============================
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

# ==============================
# MEMORIA SIMPLE
# ==============================
historial = []

# ==============================
# FUNCIÓN IA
# ==============================
def responder_ia(mensaje):
    global historial

    historial.append({"role": "user", "content": mensaje})
    historial = historial[-6:]

    system_prompt = (
        "Eres sembrIA 🌱, un asistente experto en agronomía y física aplicada.\n\n"

        "OBJETIVO:\n"
        "Ayudar a comprender la conservación de la energía mecánica aplicada a la agronomía,\n"
        "desde lo más básico hasta lo más avanzado.\n\n"

        "ESTILO OBLIGATORIO:\n"
        "- Conversacional, natural y cercano.\n"
        "- Escribe como un profesor que explica con calma.\n"
        "- Habla de tú.\n"
        "- Usa emojis libremente cuando aporten claridad o cercanía.\n"
        "- Varía los emojis.\n"
        "- Usa emojis relacionados con agronomía, agua, suelo, energía, campo y maquinaria.\n\n"

        "PROHIBIDO:\n"
        "- NO uses listas numeradas.\n"
        "- NO uses símbolos como #1, #2, 1), 2).\n"
        "- NO escribas como manual técnico.\n"
        "- NO seas robótico.\n\n"

        "FORMA DE ORGANIZAR IDEAS:\n"
        "- Separa ideas con saltos de línea.\n"
        "- Usa frases claras.\n"
        "- Introduce ideas con texto.\n\n"

        "CUANDO USES FÓRMULAS:\n"
        "- Escríbelas claras y legibles.\n"
        "- Usa * para multiplicar y ^ para potencias.\n"
        "- Evita símbolos compactos.\n\n"

        "FORMATO DE FÓRMULAS:\n"
        "Ec = (1 / 2) * m * v^2\n"
        "Ep = m * g * h\n"
        "Em = Ep + Ec\n\n"

        "SI RESUELVES UN PROBLEMA:\n"
        "- Explica primero con palabras.\n"
        "- Luego muestra la fórmula.\n"
        "- Explica variables.\n"
        "- Interpreta el resultado en contexto agrícola.\n\n"

        "REGLAS:\n"
        "- No repitas saludos.\n"
        "- No te salgas del tema de energía mecánica aplicada a agronomía.\n"
        "- Mantén coherencia académica.\n\n"

        "CIERRE:\n"
        "- Nunca termines abruptamente.\n"
        "- Cierra con una invitación natural a seguir aprendiendo."
    )

    messages = [
        {"role": "system", "content": system_prompt}
    ] + historial

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.6,
        max_tokens=850
    )

    respuesta = response.choices[0].message.content

    historial.append({"role": "assistant", "content": respuesta})
    historial = historial[-6:]

    return respuesta


# ==============================
# LÓGICA GENERAL
# ==============================
def responder(mensaje):
    texto = mensaje.lower().strip()

    if texto in ["hola", "buenas", "hey"]:
        return (
            "👋 ¡Hola! Soy sembrIA 🌱\n\n"
            "Estoy aquí para ayudarte con la conservación de la energía mecánica aplicada a la agronomía.\n\n"
            "Haz tu pregunta y la analizamos juntos 🚜⚙️"
        )

    return responder_ia(mensaje)


# ==============================
# RUTAS
# ==============================
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    mensaje = data.get("mensaje", "")
    respuesta = responder(mensaje)
    return jsonify({"respuesta": respuesta})


# ==============================
# EJECUCIÓN
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
