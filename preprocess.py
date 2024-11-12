# preprocess.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split

def load_data():
    user_data = pd.read_csv('data/user_data.csv')
    event_data = pd.read_csv('data/event_data.csv')
    interaction_data = pd.read_csv('data/interaction_data.csv')
    return user_data, event_data, interaction_data

def preprocess_data(user_data, event_data, interaction_data):
    # Encode categorical features
    user_data['interest'] = LabelEncoder().fit_transform(user_data['interest'])
    event_data['event_type'] = LabelEncoder().fit_transform(event_data['event_type'])

    # Normalize user_id and event_id
    interaction_data['user_id'] = interaction_data['user_id'] - interaction_data['user_id'].min()
    interaction_data['event_id'] = interaction_data['event_id'] - interaction_data['event_id'].min()

    # Merge data
    interaction_data = interaction_data.merge(user_data, on='user_id').merge(event_data, on='event_id')
    interaction_data['interaction'] = 1

    # Split data
    train_data, test_data = train_test_split(interaction_data, test_size=0.2, random_state=42)

    # Scale features
    scaler = MinMaxScaler()
    user_features = scaler.fit_transform(user_data[['age', 'interest']])
    event_features = scaler.fit_transform(event_data[['event_type']])
    
    return train_data, test_data, scaler

if __name__ == "__main__":
    user_data, event_data, interaction_data = load_data()
    train_data, test_data, scaler = preprocess_data(user_data, event_data, interaction_data)
