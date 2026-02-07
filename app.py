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
# CARGAR CONOCIMIENTO
# ==============================
def cargar_conocimiento():
    textos = []
    for archivo in ["basico.txt", "intermedio.txt", "avanzado.txt"]:
        ruta = os.path.join("conocimiento", archivo)
        with open(ruta, "r", encoding="utf-8") as f:
            textos.append(f.read())
    return "\n\n".join(textos)

CONOCIMIENTO = cargar_conocimiento()

# ==============================
# MEMORIA DE CONVERSACIÓN
# ==============================
historial = []

# ==============================
# RESPUESTA CON IA
# ==============================
def responder_ia(mensaje):
    global historial

    historial.append({"role": "user", "content": mensaje})
    historial = historial[-6:]

    system_prompt = (
        "Eres sembIA 🌱, un asistente experto en agronomía y física aplicada.\n\n"

        "OBJETIVO:\n"
        "Ayudar a comprender la conservación de la energía mecánica aplicada a la agronomía,\n"
        "desde lo más básico hasta lo más avanzado.\n\n"

        "ESTILO OBLIGATORIO:\n"
        "- Conversacional, natural y cercano.\n"
        "- Escribe como un profesor que explica con calma.\n"
        "- Habla de tú.\n"
        "- Usa emojis libremente cuando aporten claridad o cercanía.\n"
        "- Varía los emojis, no repitas siempre los mismos.\n"
        "- Usa emojis relacionados con agronomía, agua, suelo, energía, campo y maquinaria.\n\n"

        "PROHIBIDO:\n"
        "- NO uses listas numeradas.\n"
        "- NO uses símbolos como #1, #2, 1), 2).\n"
        "- NO escribas como manual técnico.\n"
        "- NO seas robótico.\n\n"

        "FORMA DE ORGANIZAR IDEAS:\n"
        "- Separa ideas con saltos de línea.\n"
        "- Usa frases cortas y claras.\n"
        "- Introduce ideas con texto, no con números.\n\n"

        "CUANDO USES FÓRMULAS:\n"
        "- Escríbelas de forma clara y legible.\n"
        "- Usa * para multiplicar y ^ para potencias.\n"
        "- Evita símbolos raros o compactos.\n\n"

        "FORMATO DE FÓRMULAS:\n"
        "Ec = (1 / 2) * m * v^2\n"
        "Ep = m * g * h\n"
        "Em = Ep + Ec\n\n"

        "SI RESUELVES UN PROBLEMA:\n"
        "- Explica primero con palabras.\n"
        "- Luego muestra la fórmula.\n"
        "- Explica qué representa cada variable.\n"
        "- Interpreta el resultado en el contexto del campo.\n\n"

        "REGLAS:\n"
        "- No repitas mensajes de bienvenida.\n"
        "- No te salgas del tema de energía mecánica en agronomía.\n"
        "- Usa solo el conocimiento proporcionado.\n\n"

        "CIERRE:\n"
        "- Nunca termines de forma brusca.\n"
        "- Cierra con una idea clara o invitación a seguir."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"CONOCIMIENTO BASE:\n{CONOCIMIENTO}"}
    ] + historial

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.4,
        max_tokens=400
    )

    respuesta = response.choices[0].message.content

    historial.append({"role": "assistant", "content": respuesta})
    historial = historial[-6:]

    return respuesta

# ==============================
# RESPUESTA GENERAL
# ==============================
def responder(mensaje):
    mensaje_original = mensaje
    mensaje = mensaje.lower().strip()

    if mensaje in ["hola", "holaa", "buenas", "hey"]:
        return (
            "👋 ¡Hola! Soy SembIA 🌱\n\n"
            "Puedo ayudarte con cualquier duda sobre la conservación de la energía mecánica "
            "aplicada a la agronomía.\n\n"
            "Pregúntame con confianza 😊"
        )

    if mensaje in ["gracias", "muchas gracias"]:
        return "😊 ¡Con gusto! Si quieres, seguimos profundizando."

    if mensaje in ["adiós", "chau", "hasta luego"]:
        return "👋 ¡Hasta luego! Aquí estaré cuando lo necesites 🌾"

    return responder_ia(mensaje_original)

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

