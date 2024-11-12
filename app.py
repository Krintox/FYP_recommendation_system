# app.py
from flask import Flask, request, jsonify
import tensorflow as tf
from recommend import recommend_events

# Load the saved model
model = tf.keras.models.load_model('ncf_recommendation_model.h5')

app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    user_id = int(data['user_id'])
    
    # Generate recommendations
    recommended_events = recommend_events(model, user_id)
    return jsonify(recommendations=recommended_events.tolist())

if __name__ == '__main__':
    app.run(port=5000, debug=True)
