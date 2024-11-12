# train_model.py
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Flatten, Dense, Concatenate
from preprocess import load_data, preprocess_data

def create_model(num_users, num_events, embedding_size=50):
    # Define user and event embeddings
    user_input = Input(shape=(1,), name='user_input')
    user_embedding = Embedding(input_dim=num_users, output_dim=embedding_size, name='user_embedding')(user_input)
    user_vec = Flatten(name='user_flatten')(user_embedding)

    event_input = Input(shape=(1,), name='event_input')
    event_embedding = Embedding(input_dim=num_events, output_dim=embedding_size, name='event_embedding')(event_input)
    event_vec = Flatten(name='event_flatten')(event_embedding)

    # Concatenate embeddings
    concat = Concatenate()([user_vec, event_vec])
    dense1 = Dense(128, activation='relu')(concat)
    dense2 = Dense(64, activation='relu')(dense1)
    output = Dense(1, activation='sigmoid')(dense2)

    model = Model(inputs=[user_input, event_input], outputs=output)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_model():
    user_data, event_data, interaction_data = load_data()
    train_data, test_data, _ = preprocess_data(user_data, event_data, interaction_data)

    num_users = user_data['user_id'].nunique()
    num_events = event_data['event_id'].nunique()

    model = create_model(num_users, num_events)
    
    train_users = train_data['user_id'].values
    train_events = train_data['event_id'].values
    train_interactions = train_data['interaction'].values

    # Train the model
    history = model.fit(
        [train_users, train_events],
        train_interactions,
        epochs=10,
        batch_size=64,
        validation_split=0.1
    )
    
    # Save the model
    model.save('ncf_recommendation_model.h5')
    print("Model training complete and saved as 'ncf_recommendation_model.h5'.")

if __name__ == "__main__":
    train_model()
