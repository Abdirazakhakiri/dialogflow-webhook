import os
from flask import Flask, request, jsonify
from openai import OpenAI

# Load OpenAI API key from environment (set in Render)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        req = request.get_json(silent=True)
        user_message = req.get("queryResult", {}).get("queryText", "")

        if not user_message:
            return jsonify({"fulfillmentText": "I didn’t catch that. Can you rephrase it?"})

        # Customize GPT-4 behavior with system message
        messages = [
            {
                "role": "system",
                "content": "You're a helpful AI assistant that answers only about halal lead generation, Facebook ads, automation, guarantees, and services. Be persuasive and concise."
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
        return jsonify({"fulfillmentText": "Oops! I ran into a glitch. Give me a sec to fix it."})

if __name__ == "__main__":
    app.run()