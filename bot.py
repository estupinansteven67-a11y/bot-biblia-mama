import os
from groq import Groq
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# --- TUS LLAVES ---
GROQ_API_KEY = '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'.strip()
TELEGRAM_TOKEN = '8628051672:AAHzQ2_9ieGnK9W_cS5GHzUNUrKiCAfm9EA'.strip()

client = Groq(api_key=GROQ_API_KEY)

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    print(f"Mamá dice: {user_text}")
    
    try:
        # CAMBIO AQUÍ: Usamos la versión 3.1 que es la activa
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system", 
                    "content": "Eres un asistente bíblico dulce para mi mamá. Explica con amor y usa MAYÚSCULAS para los versículos."
                },
                {"role": "user", "content": user_text}
            ]
        )
        
        respuesta = completion.choices[0].message.content
        await update.message.reply_text(respuesta)
        print(">>> ¡POR FIN ENVIADO!")

    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("Mami, el sistema se está actualizando. Prueba en un segundo.")

if __name__ == '__main__':
    print("--- CONECTANDO CON LLAMA 3.1 ---")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))
    app.run_polling()