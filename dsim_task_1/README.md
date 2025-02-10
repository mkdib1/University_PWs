# Structure
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
|     |- dataset_building.ipynb   		# building a pandas dataframe and writing eeg.csv, starting from extracting data from zip folders after downloading
|     |- eeg.csv  				# arrenged dataset
|  |- .env 					# environment variables setting
|  |- requirements.txt 				# libraries and packages installation guidelines
|  |- README.md 				# this file
```
   

# Set env var
After downloading the folder, please open the .env file and set the `BASE_DIR` variable by replacing the default string with your local path.