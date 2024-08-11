import os
import shutil
import cv2
import boto3
import numpy as np
import pandas as pd

# Set the file paths for the unprocessed and processed file locations
unprocessed_dir = 'Unprocessed/'
processed_dir = 'Processed/'

# Set up the AWS credentials
session = boto3.Session(
    aws_access_key_id='AWS_ACCESS_KEY_ID',
    aws_secret_access_key='AWS_SECRET_ACCESS_KEY',
)
# Create an S3 client
s3 = session.client('s3')

# Loop through all files in the unprocessed directory
for filename in os.listdir(unprocessed_dir):
    if filename.endswith('.mp4'):
        filepath = os.path.join(unprocessed_dir, filename)
        #file_name extract from the file we are using.
        file_name = os.path.basename(filename)

        cap = cv2.VideoCapture(filepath)

        #dataframe configure
        df = pd.DataFrame(columns =['X'])

        # initialize variables for motion detection
        ret, frame1 = cap.read()
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

        # initialize variables for counting motion changes
        total_motion_changes = []

        while True:
            # read frame from video
            ret, frame2 = cap.read()

            # break if no frame is read
            if not ret:
                break

            # convert frame to grayscale and apply Gaussian blur
            gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

            # calculate difference between two frames
            frame_diff = cv2.absdiff(gray1, gray2)

            # apply threshold to the frame difference
            threshold = cv2.threshold(frame_diff, 20, 255, cv2.THRESH_BINARY)[1]

            # count the number of white pixels in the thresholded image
            motion_changes = cv2.countNonZero(threshold)

            # append the number of motion changes to the list
            total_motion_changes.append(motion_changes)

            # set current frame as the previous frame for the next iteration
            gray1 = gray2.copy()

            # display video and thresholded frames
            # cv2.imshow('Video', frame2)
            # cv2.imshow('Threshold', threshold)

            if cv2.waitKey(1) == ord('q'):
                break

        # release video capture object and close windows
        cap.release()
        cv2.destroyAllWindows()

        # print the total number of motion changes per frame
        for i, motion_changes in enumerate(total_motion_changes):
            df.loc[len(df)] = motion_changes

        # get total entries
        total_entries = len(df)

        # get average of all entries
        avg_entries = df.mean()[0]

        # get sum of highest 100 entries
        if df['X'].dtype == 'object':
            df['X'] = pd.to_numeric(df['X'], errors='coerce')

        sum_highest_1000 = df.nlargest(1000, 'X')['X'].sum()

        # create a new data frame with the three values
        new_df = pd.DataFrame({'total_entries': [total_entries], 'avg_entries': [avg_entries], 'sum_highest_100': [sum_highest_1000]})

        # sending DFs to S3 Bucket
        csv_buffer = new_df.to_csv(index=False)
        bucket_name = 'surf.tracking.data.csv'
        folder_path = 'Motion Change Tracker/'
        file_name_s3 = str(file_name) + '.csv'
        file_path_s3 = folder_path + file_name_s3
        s3.put_object(
            Bucket='surf.tracking.data.csv',
            Key=file_path_s3,
            Body=csv_buffer.encode()
        )
        processed_filepath = os.path.join(processed_dir, filename)
        shutil.move(filepath, processed_filepath)