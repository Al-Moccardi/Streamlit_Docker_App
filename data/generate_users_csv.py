import pandas as pd
import random
import string

# Function to generate a random username
def generate_username():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

# Function to generate a random password
def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# Number of instances you want to create
num_instances = 1000

# Generate data
data = []
for _ in range(num_instances):
    data.append({
        'username': generate_username(),
        'password': generate_password(),
        'age': random.randint(18, 70),  # Age range from 18 to 70
        'annual_income': random.randint(1, 150),  # Annual income in thousands
        'spending_score': random.randint(1, 100)  # Spending score from 1 to 100
    })

# Create DataFrame
df = pd.DataFrame(data)

# Define the CSV file path
csv_file_path = 'users.csv'

# Save the DataFrame to a CSV file
df.to_csv(csv_file_path, index=False)

print(f"CSV file with {num_instances} instances has been created and saved to {csv_file_path}")
