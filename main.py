import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Render y otros servicios usan variables de entorno por seguridad
# En Render configurarás GOOGLE_API_KEY en la sección 'Environment'
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
genai.configure(api_key=api_key)

# Configuración del modelo
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    pregunta_cliente = data.get("pregunta")
    
    contexto = """
    Eres el asistente experto de Moises Rodriguez, un desarrollador Web y Diseñador frontend.
    Tu objetivo es ayudar a los clientes con dudas sobre:
    - Diseño web profesional (Framer, WordPress, Divi).
    - Creacion de branding y logos.
    - Asistencia para soporte en WhatsApp y otras redes sociales.
    
    Si preguntan por el dueño, menciona que es un experto en optimización digital.
    Responde de forma breve, amable y profesional. 
    Si el cliente parece interesado en contratar, dile que puede agendar una consultoría pulsando el botón "AGENDAR CITA".

    ### PLANTILLA DE PRECIOS Y SERVICIOS:
    - Diseño Web Landing Page (Framer): Desde $250 USD.
    - Tienda E-commerce (WooCommerce + WhatsApp): Desde $450 USD.
    - Mantenimiento Mensual: a partir de $80 USD/mes.
    - Branding: a partir de 100$ USD.
    - Guia de Marca: a partir de 150$ USD.
    - Posts/Historias: $10 USD c/u.
    - Bots personalizados: Consultar vía email a moisesmiguel.r.contacto@gmail.com.

    ### GUION DE VENTAS:
    - Si preguntan por métodos de pago: Aceptamos Bolívares (BCV), divisas electrónicas o Binance.
    - ¡PROMO!: Pagos con Binance o Efectivo tienen 15% de descuento.
    - Al finalizar sobre precios, pregunta: "¿Te gustaría que agendemos una cita para aterrizar tu proyecto?"
    """

    try:
        prompt_final = f"{contexto}\n\nCliente: {pregunta_cliente}\nAsistente:"
        response = model.generate_content(prompt_final)
        return jsonify({"respuesta": response.text})
    except Exception as e:
        print(f"Error: {e}") # Para que puedas ver el error en los logs de Render
        return jsonify({"respuesta": "Lo siento, tuve un pequeño problema técnico. ¿Puedes repetir?"}), 500

if __name__ == '__main__':
    # Esto permite que Render elija el puerto automáticamente
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
