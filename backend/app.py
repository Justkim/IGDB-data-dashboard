from flask import Flask, request, jsonify
import game_recommender
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
@app.route('/recommend', methods=['POST'])
def recommend_games():
    data = request.get_json()
    text = data.get('text', '')
    try:
        recommendations = game_recommender.get_recommended_games(text)
        response = jsonify({'recommendations': recommendations}), 200
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except exception as e:
        print("wow")
        response = jsonify({'error': str(e)}), 500
        return  response.headers.add('Access-Control-Allow-Origin', '*')
    
if __name__ == "__main__":
    app.run(debug=True, port=5001)
    