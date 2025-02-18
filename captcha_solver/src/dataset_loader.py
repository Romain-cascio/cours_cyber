import cv2
import numpy as np
import os
import config  # Assure-toi que config est bien importé

def load_captcha_images(dataset_path):
    images = []
    labels = []
    
    for filename in os.listdir(dataset_path):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            image_path = os.path.join(dataset_path, filename)
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            
            # Vérifier si l'image est bien chargée
            if img is None:
                print(f"❌ ERREUR : Impossible de charger l'image {image_path}, elle sera ignorée.")
                continue  # Passe à l'image suivante sans planter

            # 🔥 Redimensionnement obligatoire
            img = cv2.resize(img, config.CAPTCHA_IMAGE_SIZE)

            # 🔥 Normalisation des pixels
            img = img / 255.0

            # Supposons que le nom du fichier = label
            label = filename.split(".")[0]  

            images.append(img)
            labels.append(label)

    print(f"✅ {len(images)} images valides chargées.")
    return np.array(images, dtype=np.float32), np.array(labels, dtype=str)
