import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Constants
num_users = 5000  # Increased number of users
num_events = 1000  # Increased number of events
num_interactions = 20000  # Increased interactions

# Generate user demographics
user_ids = np.arange(1, num_users + 1)
user_ages = np.random.randint(18, 60, size=num_users)
user_locations = np.random.choice(['Urban', 'Suburban', 'Rural'], size=num_users)
user_interests = np.random.choice(['Cleaning', 'Recycling', 'Education', 'Community', 'Wildlife'], size=num_users)

# Generate event features
event_ids = np.arange(1, num_events + 1)
event_types = np.random.choice(['Beach Cleanup', 'Park Cleanup', 'Educational Workshop', 'Recycling Drive'], size=num_events)
event_dates = pd.date_range(start='2024-01-01', periods=num_events, freq='7D')
event_locations = np.random.choice(['Location A', 'Location B', 'Location C'], size=num_events)
event_descriptions = [f"{event_type} happening at {location}." for event_type, location in zip(event_types, event_locations)]

# Generate random interactions
data = {
    'user_id': np.random.choice(user_ids, num_interactions),
    'event_id': np.random.choice(event_ids, num_interactions),
    'interaction': np.random.choice(['like', 'share', 'comment'], num_interactions),
}

# Create user and event dataframes
user_data = pd.DataFrame({
    'user_id': user_ids,
    'age': user_ages,
    'location': user_locations,
    'interest': user_interests
})

event_data = pd.DataFrame({
    'event_id': event_ids,
    'event_type': event_types,
    'event_date': event_dates,
    'location': event_locations,
    'description': event_descriptions
})

# Create interaction DataFrame
interaction_data = pd.DataFrame(data)

# Show the first few rows of each DataFrame
print("User Data:")
print(user_data.head())
print("\nEvent Data:")
print(event_data.head())
print("\nInteraction Data:")
print(interaction_data.head())

# Save to CSV files
user_data.to_csv('user_data.csv', index=False)
event_data.to_csv('event_data.csv', index=False)
interaction_data.to_csv('interaction_data.csv', index=False)
