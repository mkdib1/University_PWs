# Image Classification with Pre-trained Models for Planets and Moons Dataset
This project focuses on image classification using pre-trained deep learning models to identify different planets and moons from the [Planets and Moons Dataset](https://www.kaggle.com/datasets/emirhanai/planets-and-moons-dataset-ai-in-space?resource=download&select=Planets_Moons_Data).

## Prerequisites
To run this notebook, you'll need the following libraries:
```python
from tensorflow import keras
from tensorflow.keras.applications import EfficientNetB3
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Dense, GlobalMaxPool2D, GlobalAveragePooling2D, Conv2D, MaxPooling2D, Flatten, Dropout, BatchNormalization, Activation
from tensorflow.keras.models import Model
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from google.colab import drive
import zipfile
from shutil import copyfile
import matplotlib.image as mpimg
from tensorflow.keras import layers
import itertools
from sklearn.metrics import confusion_matrix
from tensorflow.keras.preprocessing import image_dataset_from_directory
from sklearn.metrics import classification_report
```

## Dataset Setup
Follow these steps to download and prepare the dataset in Google Colab:
1. Mount your Google Drive:
```python
from google.colab import drive
drive.mount('/content/drive', force_remount=True)
```
2. Download the dataset from Kaggle:
```python
!kaggle datasets download -d emirhanai/planets-and-moons-dataset-ai-in-space
```
3. Unzip the dataset:
```python
# If downloading directly
!unzip planets-and-moons-dataset-ai-in-space.zip -d ./dataset
# If using from Drive
!unzip "/content/drive/MyDrive/path_to_your_file/planets-and-moons-dataset.zip" -d ./dataset
```

## Running the best model
To test the pre-trained model, you need to access the `models.zip` file from Google Drive. The pre-trained model file is available at this link: [Models.zip](https://drive.google.com/file/d/1dcA5uFx_Dw5bsPNNhLIa1Xz1Bxh72q-n/view?usp=drive_link).

Follow these steps to download and use the pre-trained model:

1. Download the models.zip file from the shared Google Drive link
2. Upload it to your Colab environment or to your own Google Drive
3. Unzip and load the model:

```python
# Option 1: If you've uploaded the file to your Google Drive
!cp "/content/drive/MyDrive/models.zip" ./
!unzip models.zip

# Option 2: Directly download from the shared link
!gdown 1dcA5uFx_Dw5bsPNNhLIa1Xz1Bxh72q-n
!unzip models.zip

# Load the pre-trained model
model = keras.models.load_model('./model_M.keras')
```

The model can then be used to make predictions on new images from the planets and moons dataset.
