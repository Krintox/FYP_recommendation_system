# recommend.py
import numpy as np
import tensorflow as tf
from preprocess import load_data, preprocess_data

def recommend_events(model, user_id, num_recommendations=5):
    user_data, event_data, _ = load_data()
    num_events = event_data['event_id'].nunique()

    # Generate recommendations
    event_ids = np.array(range(num_events))
    user_ids = np.array([user_id] * num_events)
    
    # Predict interaction likelihoods for the user with all events
    scores = model.predict([user_ids, event_ids])
    top_event_indices = np.argsort(scores.flatten())[-num_recommendations:][::-1]

    recommended_events = event_data.iloc[top_event_indices]['event_id'].values
    return recommended_events

if __name__ == "__main__":
    model = tf.keras.models.load_model('ncf_recommendation_model.h5')
    user_id = 0  # Example user ID
    recommendations = recommend_events(model, user_id)
    print("Recommended events:", recommendations)
