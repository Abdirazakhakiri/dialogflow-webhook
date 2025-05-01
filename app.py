import os
from flask import Flask, request, jsonify
from openai import OpenAI

# Create the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "sk-REPLACE_ME_WITH_YOUR_KEY"))

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        req = request.get_json(silent=True)
        user_message = req.get("queryResult", {}).get("queryText", "")

        if not user_message:
            return jsonify({"fulfillmentText": "I didn’t catch that. Can you rephrase?"})

        # Call the new OpenAI client
        response = client.chat.completions.create(
            model="gpt-4",  # You can change to "gpt-3.5-turbo" if needed
            messages=[
                {"role": "system", "content": "You are a helpful chatbot that helps small business owners grow."},
                {"role": "user", "content": user_message}
            ]
        )

        bot_reply = response.choices[0].message.content.strip()

        return jsonify({"fulfillmentText": bot_reply})

    except Exception as e:
        print("⚠️ Webhook Error:", str(e))
        return jsonify({"fulfillmentText": "Something went wrong on my end. Hang tight while I fix it!"})

if __name__ == "__main__":
    app.run()