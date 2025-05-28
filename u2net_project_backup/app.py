from flask import Flask, request, send_file
import os
from io import BytesIO
from remove_background import remove_background  # Asegúrate de que este archivo exista en la misma carpeta o ajusta la ruta

app = Flask(__name__)

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return "No se proporcionó la imagen", 400

    image_file = request.files['image']
    
    # Guarda la imagen temporalmente
    input_path = "temp_input.jpg"
    output_path = "temp_output.png"
    image_file.save(input_path)
    
    # Procesa la imagen usando la función remove_background
    try:
        remove_background(input_path, output_path)
    except Exception as e:
        return f"Error procesando la imagen: {e}", 500

    # Envía la imagen procesada al cliente
    return send_file(output_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
