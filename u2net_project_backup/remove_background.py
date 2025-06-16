import torch
from torchvision import transforms
from PIL import Image
import cv2
import numpy as np
import os
from model.u2net import U2NET  # Asegúrate de tener este archivo en tu proyecto

# Ruta al modelo preentrenado U-2-Net
model_path = "saved_models/u2net/u2net.pth"

# Instanciar el modelo y cargar los pesos
print("Cargando el modelo...")
try:
    model = U2NET(3, 1)
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    print("✅ Modelo cargado correctamente.")
except Exception as e:
    print("❌ Error al cargar el modelo:", e)

# Función para eliminar el fondo de una imagen
def remove_background(image_path, output_path):
    if not os.path.exists(image_path):
        print(f"❌ La imagen {image_path} no existe.")
        return

    print("🖼️ Cargando la imagen...")
    image = Image.open(image_path).convert("RGB")

    print("🔄 Preprocesando la imagen...")
    transform = transforms.Compose([
        transforms.Resize((320, 320)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    image_tensor = transform(image).unsqueeze(0)

    print("🧠 Procesando con el modelo...")
    with torch.no_grad():
        d1, *_ = model(image_tensor)

    print("🎭 Procesando la predicción...")
    prediction = d1[0][0].cpu().numpy()
    prediction = (prediction - prediction.min()) / (prediction.max() - prediction.min() + 1e-8)
    mask = (prediction > 0.5).astype(np.uint8) * 255

    print("🪄 Aplicando transparencia...")
    image = image.resize((320, 320))
    image_array = np.array(image)
    alpha = Image.fromarray(mask).resize(image.size)
    rgba_image = image.convert("RGBA")
    rgba_image.putalpha(alpha)

    print(f"💾 Guardando resultado en {output_path}...")
    rgba_image.save(output_path)
    print("✅ ¡Fondo eliminado exitosamente!")

# Ruta de entrada y salida
input_image = "assets/images/blusaroja.jpg"
output_image = "assets/images/blusaroja_out.png"

# Ejecutar
remove_background(input_image, output_image)

# Mostrar la imagen
try:
    Image.open(output_image).show()
except Exception as e:
    print(f"No se pudo mostrar la imagen automáticamente. Error: {e}")
