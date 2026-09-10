from flask import Flask, render_template, request, send_file, jsonify, send_from_directory
from PIL import Image, ImageOps
import io
import os
from datetime import datetime  # Para nomes de arquivo únicos

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

imagem_atual = None
current_image_path = None


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    global imagem_atual, current_image_path

    if 'image' not in request.files:
        return jsonify({"error": "Nenhuma imagem enviada"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Nenhuma imagem selecionada"}), 400

    # Gerar nome único para o arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    file.save(path)
    imagem_atual = Image.open(path)
    current_image_path = path

    return jsonify({"path": f"/{path}"})


@app.route('/edit', methods=['POST'])
def edit():
    global imagem_atual, current_image_path

    if imagem_atual is None:
        return jsonify({"error": "Nenhuma imagem carregada"}), 400

    action = request.json.get('action')

    if action == 'rotate_left':
        imagem_atual = imagem_atual.rotate(90, expand=True)
    elif action == 'rotate_right':
        imagem_atual = imagem_atual.rotate(-90, expand=True)
    elif action == 'black_white':
        imagem_atual = imagem_atual.convert('L')
    elif action == 'sepia':
        sepia = ImageOps.colorize(
            imagem_atual.convert('L'), '#704214', '#C0A080')
        imagem_atual = sepia

    # Salvar a imagem editada no mesmo caminho
    imagem_atual.save(current_image_path)

    # Retornar o novo caminho com timestamp para evitar cache
    return jsonify({"path": f"/{current_image_path}?t={datetime.now().timestamp()}"})


@app.route('/save', methods=['POST'])
def save_image():
    global imagem_atual, current_image_path

    if imagem_atual is None:
        return jsonify({"error": "Nenhuma imagem para salvar"}), 400

    try:
        # Cria um nome único para o arquivo salvo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_filename = f"foto_salva_{timestamp}.jpg"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], save_filename)

        # Salva a cópia da imagem editada
        imagem_atual.save(save_path)

        # Força o download no navegador
        return send_from_directory(
            directory=app.config['UPLOAD_FOLDER'],
            path=save_filename,
            as_attachment=True,
            mimetype='image/jpeg'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
