import boto3
import pandas as pd

# Set up the AWS credentials
session = boto3.Session(
    aws_access_key_id='AWS_ACCESS_KEY_ID',
    aws_secret_access_key='AWS_SECRET_ACCESS_KEY',
)

# Initialize S3 client and bucket name
s3_client = boto3.client('s3')
bucket_name = 'surf.tracking.data.csv'

# Define CSV file name and key
csv_file_name = 'GS_JR_0.43.mp4.csv'
csv_file_key = 'https://s3.eu-west-2.amazonaws.com/surf.tracking.data.csv/GS_JR_0.43.mp4.csv'

# Download CSV file from S3 bucket
response = s3_client.get_object(Bucket=bucket_name, Key=csv_file_key)
csv_data = response['Body'].read().decode('utf-8')

# Load CSV data into pandas DataFrame
df = pd.read_csv(pd.compat.StringIO(csv_data))

# Calculate average of each column
column_averages = df.mean()

# Calculate average change between each row of each column
row_diffs = df.diff().mean()

# Print results
print("Average of each column:")
print(column_averages)

print("Average change between each row of each column:")
print(row_diffs)
