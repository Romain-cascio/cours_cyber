from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Dropout, Reshape
import config
import dataset_loader
import numpy as np

def encode_labels_one_hot(labels):
    """Convertit chaque label en encodage one-hot"""
    max_length = max(len(label) for label in labels)  # Longueur max d'un CAPTCHA
    encoded_labels = np.zeros((len(labels), max_length, len(config.CHARACTERS)), dtype=np.float32)

    for i, label in enumerate(labels):
        for j, char in enumerate(label):
            index = config.CHAR_TO_INDEX[char]
            encoded_labels[i, j, index] = 1  # Encodage one-hot

    return encoded_labels

def train_captcha_solver():
    images, labels = dataset_loader.load_captcha_images(config.DATASET_PATH)

    images = images / 255.0  # Normalisation des pixels
    max_label_length = max(len(label) for label in labels)  # Nombre max de caractères par CAPTCHA

    # 🔥 Convertir les labels en one-hot encoding
    encoded_labels = encode_labels_one_hot(labels)

    model = Sequential([
        Conv2D(32, (3,3), activation='relu', input_shape=(config.CAPTCHA_IMAGE_SIZE[0], config.CAPTCHA_IMAGE_SIZE[1], 1)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(max_label_length * len(config.CHARACTERS), activation='softmax'),  # Prédiction multiple
        Reshape((max_label_length, len(config.CHARACTERS)))  # Reformate la sortie
    ])
    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(images, encoded_labels, epochs=10, validation_split=0.2)
    model.save(config.MODEL_PATH)

    print(f"✅ Modèle entraîné et sauvegardé dans {config.MODEL_PATH}")

if __name__ == "__main__":
    train_captcha_solver()
