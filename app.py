import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        req = request.get_json(silent=True)
        user_message = req.get("queryResult", {}).get("queryText", "")

        if not user_message:
            return jsonify({"fulfillmentText": "I didn’t catch that. Can you rephrase it?"})

        # 🔍 Debug the environment variable before using it
        print("🔍 ENV CHECK — OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))

        # Use the OpenAI client
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # ChatGPT behavior
        messages = [
            {
                "role": "system",
                "content": "You're a helpful assistant for business owners. Keep answers short and smart."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )

        bot_reply = response.choices[0].message.content.strip()
        return jsonify({"fulfillmentText": bot_reply})

    except Exception as e:
        print("❌ Webhook Error:", str(e))
        return jsonify({"fulfillmentText": "Oops! Something went wrong on my end. Please try again later."})

if __name__ == "__main__":
    app.run()