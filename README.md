# Risk-Based Authentication using Browser Fingerprints

Machine learning model for detecting suspicious login attempts using browser fingerprint and network data.

## Overview

This project classifies login attempts as **legitimate or suspicious** using browser fingerprint features.  
The goal is to improve security while minimizing false positives.

## Features

- Random Forest classifier
- Browser fingerprint-based features
- Confusion matrix and F1 score evaluation
- Feature importance analysis

## Dataset

The model uses labeled login data with features such as:

- IP Address  
- Browser and OS  
- Device Type  
- Attack indicators  
- Account takeover flags  

Target:
- `Login Successful` (binary classification)

## Methodology

- Split data into training and testing sets (80/20)
- Trained Random Forest model (100 trees)
- Evaluated using accuracy, F1 score, and confusion matrix
- Analyzed false positives and feature importance

## Results

- Accuracy: ~66%  
- F1 Score: ~0.60  
- Demonstrates challenges of real-world, noisy authentication data  

## Instructions

```bash
# Install dependencies
pip install -r requirements.txt

# Run the model
python model.py
