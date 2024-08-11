# Predictive Model for Competitive Surfing Scores
This repository contains a collection of Python scripts and tools developed to create a predictive model for scoring competitive surfing performances. The goal of this project is to develop a model that can accurately predict a surfer's wave score on a scale of 1 to 10, a task typically done by multiple judges and often subject to inconsistency.

# Project Overview
Competitive surfing scoring can be highly subjective, with judges often providing different scores for the same wave. This project aims to reduce this inconsistency by leveraging data analysis and machine learning techniques to predict surfing scores based on objective criteria.

# Key Components
Data Retrieval and Preprocessing:

- Scripts are provided to download and preprocess surf-related data from AWS S3 buckets.
- Features such as wave height, speed, and other relevant metrics are extracted and processed for model training.
Predictive Modeling:

- A linear regression model is trained on historical surfing data to predict scores based on various features.
- The model's coefficients and predictions are analyzed to understand the key factors influencing the scores.
Video Analysis and Object Tracking:

- Video processing scripts are included to track surfers and analyze their movements.
- Techniques like background subtraction and Gaussian blurring are applied to isolate the surfer from the video background and enhance feature detection.
Data Visualization:

- Tools for visualizing the relationship between surfing features and scores, such as scatter plots of wave height versus score.
- Real-time visualization of video processing to ensure accurate object tracking.
# Why This Matters
The scoring of competitive surfing is inherently subjective, leading to potential biases and inconsistencies in the evaluation of surfers' performances. By using machine learning and data analysis, this project seeks to provide a more objective and consistent approach to scoring, which could complement the existing judging process or even provide a fully automated scoring system.

# Future Work
- Model Enhancement: Explore more advanced machine learning models, such as neural networks, to improve predictive accuracy.
- Feature Engineering: Incorporate additional features, such as wave speed, surfer position, and aerial maneuvers, to enhance the model's performance.
- Real-time Scoring: Implement real-time scoring based on live video feeds, potentially providing immediate feedback during competitions.
# License
This project is licensed under the MIT License.
