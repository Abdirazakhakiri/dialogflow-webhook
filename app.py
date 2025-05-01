import os
from flask import Flask, request, jsonify
import openai

# Set up the Flask app
app = Flask(__name__)

# Get your OpenAI API key from environment variable (or hardcode it if testing only)
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-REPLACE_ME_WITH_YOUR_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(silent=True)
    user_message = req.get("queryResult", {}).get("queryText", "")

    if not user_message:
        return jsonify({"fulfillmentText": "I didn’t catch that. Can you try rephrasing?"})

    try:
        # Send message to OpenAI GPT-4
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for a digital marketer helping halal businesses get more leads."},
                {"role": "user", "content": user_message}
            ]
        )

        # Extract the response from GPT-4
        reply = completion.choices[0].message["content"].strip()

        return jsonify({"fulfillmentText": reply})

    except Exception as e:
        print("Error:", e)
        return jsonify({"fulfillmentText": "Something went wrong. Please try again later."})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
