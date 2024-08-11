import boto3
import pandas as pd
from io import StringIO
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt


# Initialize the S3 client
s3_client = boto3.client('s3', aws_access_key_id='AWS_ACCESS_KEY_ID', aws_secret_access_key='AWS_SECRET_ACCESS_KEY')

# Define the bucket and directory where your CSV files are stored
bucket_name = 'surf.tracking.data.csv'
directory = 'Motion Change Tracker'

# Initialize an empty DataFrame to store the data
df_all_files = pd.DataFrame()

# List all objects in the S3 bucket's directory
response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=directory)

# Loop through each object and read the contents into a DataFrame
for obj in response['Contents']:
    key = obj['Key']
    if key.endswith('.csv'):
        obj = s3_client.get_object(Bucket=bucket_name, Key=key)
        contents = obj['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(contents))

        # Extract the string from the filename and add it as a new column in the DataFrame
        filename = key.split('/')[-1]  # extract the filename from the full key path
        score = filename.split('_')[1].split('.')[0:2]  # extract the string from the filename
        score = '.'.join(score)[:4]  # stop the split two characters after the "."
        df = df.assign(Score=score)  # add the string as a new column in the DataFrame

        # Append the data to the DataFrame containing all files
        df_all_files = df_all_files.append(df)

# Convert 'Score' to numeric values
df_all_files['Score'] = pd.to_numeric(df_all_files['Score'], errors='coerce')

# Split the data into training and test sets
X = df_all_files[['total_entries', 'avg_entries', 'sum_highest_100']]
y = df_all_files['Score']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Fit a linear regression model
reg = LinearRegression().fit(X_train, y_train)

# Evaluate the model performance on the training set
y_train_pred = reg.predict(X_train)
mse_train = mean_squared_error(y_train, y_train_pred)
rmse_train = mean_squared_error(y_train, y_train_pred, squared=False)
mae_train = mean_absolute_error(y_train, y_train_pred)

# Evaluate the model performance on the test set
y_test_pred = reg.predict(X_test)
mse_test = mean_squared_error(y_test, y_test_pred)
rmse_test = mean_squared_error(y_test, y_test_pred, squared=False)
mae_test = mean_absolute_error(y_test, y_test_pred)

# Print the R-squared value of the model on the training and test sets
print('Training R-squared:', reg.score(X_train, y_train))
print('Test R-squared:', reg.score(X_test, y_test))

# Print the RMSE and MAE metrics for the model on the training and test sets
print('Training RMSE:', rmse_train)
print('Test RMSE:', rmse_test)
print('Training MAE:', mae_train)
print('Test MAE:', mae_test)

# Plot y_test vs y_test_pred on a scatter plot with axes from 0 to 10
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_test_pred, color='blue', edgecolor='k', alpha=0.6)
plt.plot([0, 10], [0, 10], color='red', lw=2)
plt.xlim(0, 10)
plt.ylim(0, 10)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted Values')
plt.grid(True)
plt.show()

