# Cross-Modal Retrieval with GAN-Based Domain Adaptation

This project implements a cross-modal retrieval system using a Generative Adversarial Network (GAN) for domain adaptation. The goal is to retrieve relevant photos given a sketch as a query.

## Project Overview

The system uses a GAN to learn a mapping between the feature spaces of sketches and photos. The GAN consists of two main components:

1. **Generator:** Takes a sketch feature vector and generates a corresponding image feature vector in the photo domain.

2. **Discriminator:** Tries to distinguish between real photo features and generated features from the generator.

The GAN is trained using adversarial loss and retrieval loss (triplet loss). The adversarial loss encourages the generator to produce features that are indistinguishable from real photo features, while the retrieval loss ensures that the generated features are similar to the features of relevant photos.

## Dataset

The project uses the Sketchy dataset, which contains a large collection of paired sketches and photos of various objects.

## Environment Setup

**Install Libraries:**

```bash
pip install transformers tensorflow numpy pandas matplotlib scikit-learn transformers
```

**Mount Google Drive:**

```python
from google.colab import drive drive.mount('/content/drive')
```

**Dataset Path:**

[Dataset Link](http://sketchy.eye.gatech.edu/)

```python
dataset_path = '/content/sketchy_data'
```

## Data Loading and Preprocessing

- Helper functions are defined to:
  - Download and extract the dataset.
  - Load and preprocess images (resizing, normalization).
  - Display batches of images.
- The dataset is loaded and preprocessed using these functions.

## Building the Encoders

1. **Image Encoder:** A pre-trained ResNet-50 model extracts 2048-dimensional features from photos.

2. **Query Encoder:** A custom CNN extracts 512-dimensional features from sketches.

## Setting Up the GAN Module

1. **Generator:** A simple feedforward neural network maps 512-dimensional sketch features to 2048-dimensional image features.

2. **Discriminator:** A simple feedforward neural network classifies image features as real or fake.

3. **Loss Functions:**

   - **Adversarial Loss:** Binary cross-entropy loss.
   - **Retrieval Loss:** Triplet loss.

4. **Optimizers:** Adam optimizer.

## Training the GAN

1. The GAN model is trained on the Sketchy dataset.

2. Callbacks save the best model weights and monitor training progress.

## Evaluation

1. The trained GAN is evaluated on a test set using retrieval accuracy (Precision@1).

## Further Improvements

1. Fine-tune the image encoder (ResNet-50).
2. Experiment with hyperparameters.
3. Explore more complex architectures.
4. Train on a larger dataset.
5. Consider other evaluation metrics (e.g., mAP).

## Conclusion

This project demonstrates a cross-modal retrieval system using a GAN for domain adaptation. The GAN aligns the feature spaces of sketches and photos, enabling retrieval of relevant photos given a sketch. Further improvements are possible.

## Acknowledgments

The project uses the Sketchy dataset and is inspired by research on cross-modal retrieval.
