import os
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Set your OpenAI API key securely from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-REPLACE_ME_WITH_YOUR_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json()
    user_message = req.get("queryResult", {}).get("queryText", "")

    if not user_message:
        return jsonify({"fulfillmentText": "I didn’t catch that. Can you try rephrasing?"})

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful marketing assistant that responds like Abdirazak Hakiri."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = completion.choices[0].message["content"]
        return jsonify({"fulfillmentText": reply})

    except Exception as e:
        return jsonify({"fulfillmentText": f"Something went wrong: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
