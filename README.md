AI-Powered Kidney Disease Prediction System

An intelligent Flask-based web application for real-time Chronic Kidney Disease (CKD) prediction and CKD stage classification using advanced Machine Learning techniques.


📌 Overview

Chronic Kidney Disease (CKD) is a progressive medical condition in which the kidneys gradually lose their ability to function effectively. Since CKD often develops silently without noticeable symptoms, early diagnosis is critical to prevent severe complications such as cardiovascular diseases and end-stage renal failure.

Traditional diagnostic approaches primarily rely on clinical indicators such as Glomerular Filtration Rate (GFR), Serum Creatinine, and Blood Urea Nitrogen (BUN). However, these approaches may fail to identify CKD during its early stages.

To address this challenge, this project presents an AI-powered diagnostic framework capable of:

* Predicting whether a patient has CKD or not.
* Determining the severity stage of CKD (Stage 1–5).
* Providing real-time predictions through an interactive web interface.
* Supporting both manual patient data entry and batch file predictions.



✨ Key Features

✅ Real-time CKD prediction using Machine Learning

✅ Binary classification (**CKD / No CKD**)

✅ Multiclass classification (**CKD Stage 1–5**)

✅ User-friendly Flask web interface

✅ Manual patient record prediction

✅ Batch prediction using CSV files

✅ Prediction history storage using SQLite database

✅ Interactive visualization charts

✅ Responsive frontend design

✅ Fast and lightweight deployment



🏥 Problem Statement

Chronic Kidney Disease affects millions of individuals worldwide and often remains undiagnosed until advanced stages. Delayed diagnosis significantly increases the risk of kidney failure and other life-threatening complications.

This project leverages Artificial Intelligence to assist healthcare professionals in identifying CKD at earlier stages, enabling timely intervention and improved patient outcomes.


🧠 Machine Learning Pipeline

The system follows the following workflow:

1. Data Collection
2. Data Cleaning and Preprocessing
3. Missing Value Handling
4. Feature Encoding
5. Outlier Detection using IQR Method
6. Feature Scaling
7. Class Imbalance Handling using SMOTE
8. Model Training
9. Model Evaluation
10. Web Deployment using Flask


🤖 Models Used

Current Web Application Models

| Task                                                 | Model    |
| ---------------------------------------------------- | -------- |
| CKD Prediction (Binary Classification)               | LightGBM |
| CKD Stage Classification (Multiclass Classification) | LightGBM |

Research Models Evaluated

* TabNet
* LightGBM
* XGBoost
* TabPFN
* CatBoost

Future Deep Learning Models for Kidney Stone Detection

* Inception-v4
* ResNet152V2
* DiET-B Transformer
* MedFuse DenseNet-Tiny


📊 Dataset Information

The system was developed using a healthcare dataset containing clinical parameters associated with Chronic Kidney Disease.

Important features include:

* Serum Creatinine
* GFR
* BUN
* Serum Calcium
* ANA
* C3/C4
* Hematuria
* Oxalate Levels
* Urine pH
* Blood Pressure
* Physical Activity
* Diet
* Water Intake
* Smoking
* Alcohol Consumption
* Family History
* Stress Level


🛠️ Technology Stack

Backend

* Python
* Flask
* SQLite

Machine Learning

* LightGBM
* Scikit-learn
* Pandas
* NumPy

Frontend

* HTML5
* CSS3
* Bootstrap
* Jinja2 Templates

Data Visualization

* Matplotlib

Version Control

* Git
* GitHub


📂 Project Structure


AI-Powered-Kidney-Disease-Prediction-System/
│
├── models/                    # Trained ML models
├── static/                    # CSS, images and generated charts
├── templates/                 # HTML templates
│
├── app.py                     # Main Flask application
├── database.py               # Database operations
├── requirements.txt          # Python dependencies
├── Procfile                  # Deployment configuration
├── test_input.csv            # Sample batch prediction file
├── .gitignore
└── README.md


⚙️ Installation and Setup

Prerequisites

* Python 3.10 or above
* Git
* VS Code (recommended)



### Step 1: Clone the Repository

```bash
git clone https://github.com/Tayyba16/AI-Powered-Kidney-Disease-Prediction-System.git
```

```bash
cd AI-Powered-Kidney-Disease-Prediction-System
```


Step 2: Create Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate environment:

Windows

```bash
venv\Scripts\activate
```

Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Step 4: Run the Application

```bash
python app.py
```

Step 5: Open in Browser

http://127.0.0.1:5000


📈 System Functionalities

Manual Prediction

Users can manually enter patient clinical information and receive instant CKD predictions.

Batch Prediction

Users can upload CSV files containing multiple patient records and obtain predictions for all records simultaneously.

Prediction History

All prediction records are stored in SQLite database for future analysis.

Visualization Dashboard

The system automatically generates visual charts to improve interpretation of prediction outcomes.



🔬 Research Contribution

This project is based on the research study:

"A Smart Diagnostic Framework for Kidney Disease Prediction Using Advanced Machine and Deep Learning Techniques"

The proposed framework integrates advanced Machine Learning algorithms to improve CKD diagnosis accuracy while providing a practical deployment through a Flask-based web application.


🚀 Future Enhancements

* Kidney Stone Detection using Deep Learning
* Medical Image Analysis (CT, MRI, Ultrasound)
* Doctor Recommendation Module
* Explainable AI (XAI)
* Cloud Deployment
* User Authentication and Authorization
* REST API Integration


👩‍💻 Author

Tayyba Ghulam Fareed

Email: [tayybaghulamfareed@gmail.com](mailto:tayybaghulamfareed@gmail.com)

GitHub: https://github.com/Tayyba16

⭐ Support

If you find this project useful, please consider giving it a star ⭐ on GitHub.



📜 License

This project is developed for educational and research purposes.
