from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/tools', methods=['GET'])
def get_tools():
    try:
        with open('tools.json', 'r') as file:
            tools_data = json.load(file)
        return jsonify(tools_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
