# Seizure EEG discrimination: a hybrid NN-ML model through signal processing in multiple domains
Starting from BONN dataset (https://www.ukbonn.de/epileptologie/arbeitsgruppen/ag-lehnertz-neurophysik/downloads/), the aim of the project is to build a model from scratch which outlies the following:
- extract handcrafted features both for time and frequency domains, after signal preprocessing
- extract neural features by feeding an architecture LSTM-based
- merge the two array-of-features for each signal in order to build a custom descriptor
- train a XGBoost classifier based on 5 classes


## 1. Structure
```
|- dsim_task_1/
|  |- data/ 					# contains 2 data subfolders
|     |- eeg_test/ 				# contains 50 .csv of test EEG tracings for predictions
|        |- eeg_1.csv
|        |- eeg_2.csv
|        |- ...
|        |- eeg_50.csv
|  |- eeg_test_class/ 			        # contains ground truth CSV
|     |- class.csv
|  |- mod/                                      # model directory
|     |- best_model_94.model 			# model to load for predictions
|     |- scaler.pkl 				# scaler for data normalization
|  |- src/  					# source code dir
|     |- demo.py   				# application script
|     |- preprocessing.py 			# data processing functions called in demo.py
|  |- utils/  					# support file dir
|     |- dataset_building.ipynb   		# notebook to extract data, build a pandas.dataframe and save it as eeg.csv
|     |- eeg.csv  				# arranged dataset
|  |- .env 					# environment variables setting
|  |- requirements.txt 				# libraries and packages installation guidelines
|  |- README.md 				# this file
```

## 2. Clone the repository
```sh
https://github.com/mkdib1/University_PWs.git
cd data-signal-and-image-processing/dsim_task_1
```

## 3. Set env var
After downloading the folder, please open the .env file and set the `BASE_DIR` variable by replacing the default string with your local path.

## 4. How to make a trial with demo
After installing requirements using
```sh
pip install -r requirements.txt
```
run `demo.py`, a gradio UI is starting on localhost: surfing the interface on the top left corner, you can choose one .csv file from `data/eeg_test` dir to check the prediction about the class of the chosen signal (ground truth is stored in `data/eeg_test_class/class.csv`)

