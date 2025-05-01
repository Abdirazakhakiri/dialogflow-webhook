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

        # Check OpenAI API Key from Environment
        api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)

        # Send to OpenAI GPT-4
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        bot_reply = response.choices[0].message.content.strip()

        return jsonify({"fulfillmentText": bot_reply})

    except Exception as e:
        print("❌ Webhook Error:", str(e))
        return jsonify({"fulfillmentText": "Oops! Something went wrong. Please try again later."})

if __name__ == "__main__":
    app.run()