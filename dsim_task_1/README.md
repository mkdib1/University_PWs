```markdown
## Structure
- **dsim_task_1/**
  - **data/** (contains 2 data subfolders)
    - **eeg_test/** (contains 50 .csv of test EEG tracings for predictions)
      - eeg_1.csv, eeg_2.csv, ..., eeg_50.csv
    - **eeg_test_class/** (contains ground truth CSV)
      - class.csv
  - **mod/** (model directory)
    - best_model_94.model (model to load for predictions)
    - scaler.pkl (scaler for normalization)
  - **src/** (source code)
    - demo.py (main script)
    - preprocessing.py (data processing functions)
  - **.env** (environment variables)
  - **requirements.txt** (installation guidelines)
  - **README.md** (this file)       

# Set env var
After downloading the folder, please enter the .env and type the right local path 
in BASE_DIR in order to SET env variables properly
