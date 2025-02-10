# Structure
dsim_task_1
│── data/   # contains 2 data subfolder
│   │── eeg_test/  # contains 50 .csv of test eeg tracings on which making predictions
│        │────── eeg_1.csv
│        │────── eeg_2.csv
│        ...
│        │────── eeg_50.csv
│   │── eeg_test_class/ # contains 1 .csv representing the ground truth of each eeg test tracing 
│        │────────── class.csv 
│
│── mod/   # model dir
│   │── best_model_94.model  # model to load for predictions
│   │── scaler.pkl  # scaler built on train data, to use for normalizing test descriptor
│
│── src/   # source code dir
│   │── __pycache__
│   │── demo.py # script for running the application
│   │── preprocessing.py # script in which are defined functions called by demo.py
│── .env  # environment variables setting, called in demo.py
│── requirements.txt  # libraries and packages installation guidelines
│── README.md         

# Set env var
After downloading the folder, please enter the .env and type the right local path 
in BASE_DIR in order to SET env variables properly
