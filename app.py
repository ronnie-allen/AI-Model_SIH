# Save this content as app.py
from flask import Flask, request, jsonify
from doamin_description import generate_detailed_paragraph
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    try:
        name = data['name']
        chosen_career = data['chosen_career']
        domain = data['domain']
        skills_known = data['skills_known']
        description = data['description']
        result = generate_detailed_paragraph(name, chosen_career, domain, skills_known, description)
        return jsonify({'response': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
