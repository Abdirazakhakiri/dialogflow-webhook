from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    query_text = data.get('queryResult', {}).get('queryText', '')

    if "leads" in query_text.lower():
        response_text = "We help you generate leads through Facebook ads and automation."
    else:
        response_text = "I'm not sure yet — but a human will follow up shortly."

    return jsonify({"fulfillmentText": response_text})


if __name__ == '__main__':
    app.run(debug=True)