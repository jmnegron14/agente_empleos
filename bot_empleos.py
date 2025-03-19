import requests
import json
from twilio.rest import Client

# 🔹 Configuración de API Keys y Twilio
JOOBLE_API_KEY = "TU_JOOBLE_API_KEY"
TWILIO_SID = "TU_TWILIO_SID"
TWILIO_AUTH_TOKEN = "TU_TWILIO_AUTH_TOKEN"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Número de Twilio para WhatsApp
MI_WHATSAPP = "whatsapp:+TU_NUMERO"  # Cambia esto con tu número de WhatsApp

# 🔹 Función para buscar empleos en Jooble
def buscar_empleos(palabra_clave, ubicacion, limite=3):
    url = f"https://jooble.org/api/{JOOBLE_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {"keywords": palabra_clave, "location": ubicacion, "page": 1, "searchMode": 1}
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        resultados = response.json().get("jobs", [])[:limite]
        return resultados
    else:
        print("Error en la API de Jooble:", response.text)
        return []

# 🔹 Función para enviar mensaje por WhatsApp
def enviar_whatsapp(empleos):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    
    if not empleos:
        mensaje = "📌 No se encontraron empleos para tu búsqueda."
    else:
        mensaje = "📌 *Nuevas ofertas de empleo:*\n\n"
        for empleo in empleos:
            mensaje += f"🔹 *{empleo['title']}*\n🏢 {empleo['company']}\n📍 {empleo['location']}\n🔗 {empleo['link']}\n\n"
    
    # Enviar mensaje a WhatsApp
    message = client.messages.create(
        body=mensaje,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=MI_WHATSAPP
    )

    print("Mensaje enviado con SID:", message.sid)

# 🔹 Ejecutar búsqueda y notificación
if __name__ == "__main__":
    empleos = buscar_empleos("Project Manager", "Madrid", limite=3)
    enviar_whatsapp(empleos)
