import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# File path
file_path = 'fingerprints.csv'

df = pd.read_csv(
    file_path,
    usecols=[
        "Login Timestamp", "User ID", "Round-Trip Time [ms]", 
        "IP Address", "Country", "Region", "City", "ASN",
        "User Agent String", "Browser Name and Version",
        "OS Name and Version", "Device Type",
        "Login Successful", "Is Attack IP", "Is Account Takeover"
    ],
    parse_dates=["Login Timestamp"],
    dtype={
        "User ID": "string",
        "IP Address": "string",
        "Country": "string",
        "Region": "string",
        "City": "string",
        "ASN": "string",
        "User Agent String": "string",
        "Browser Name and Version": "string",
        "OS Name and Version": "string",
        "Device Type": "category",
        "Login Successful": "category",
        "Is Attack IP": "category",
        "Is Account Takeover": "category",
    }
)

# threshold for missing values
threshold = 0.5

# Drop missing value columns
df = df.loc[:, df.isnull().mean() <= threshold]

# drop low value cols
df = df.drop(columns=['Country', 'Region', 'City', 'ASN', 'User Agent String', 'Login Timestamp'])

# Convert true/false to 1/0
boolean_columns = ["Login Successful", "Is Attack IP", "Is Account Takeover"]
df[boolean_columns] = df[boolean_columns].apply(lambda x: x == "True").astype(int)

# Fill missing device types
df['Device Type'] = df['Device Type'].fillna('unknown')

# Remove dots from the IP addresses
df['IP Address'] = df['IP Address'].str.replace('.', '', regex=False).astype(int)

# Scale IPs to decimal
scaler = MinMaxScaler()
df['IP Address'] = scaler.fit_transform(df[['IP Address']])

# Apply hashing to create unique integer values for each string
df['Browser Name and Version'] = df['Browser Name and Version'].apply(lambda x: hash(x) % (10 ** 8)) 
df['OS Name and Version'] = df['OS Name and Version'].apply(lambda x: hash(x) % (10 ** 8))

# Define the mapping for device types
device_type_mapping = {
    "desktop": 1,
    "tablet": 2,
    "mobile": 3,
    "bot": 4,
    "unknown": 5
}

# Replace the device type values with the corresponding numbers
df["Device Type"] = df["Device Type"].map(device_type_mapping)


# Save the processed DataFrame to a CSV file
df.to_csv('processed_fingerprints.csv', index=False)
