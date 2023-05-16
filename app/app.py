from flask import Flask, jsonify, request
from flask_cors import CORS
import chatbot_utils

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def chatbot():
    return 'Hola, ¿Cómo puedo ayudarte?'


@app.route('/message', methods=['POST'])
def message():
    try:
        # Obtener el mensaje del usuario desde la solicitud POST
        user_message = request.json.get('message')

        if user_message:
            # Procesar el mensaje del usuario
            message_bot = chatbot_utils.chatbot_cognitivo(user_message)
            response = {'message': message_bot}
            status_code = 200
        else:
            response = {'message': None}
            status_code = 400

        # Devolver la respuesta al usuario con el status code correspondiente
        return jsonify(response), status_code

    except KeyError:
        # Manejar errores en caso de que 'message' no se encuentre en la solicitud POST
        return jsonify({'error': 'Mensaje no encontrado en la solicitud POST.'}), 400

    except Exception as e:
        # Manejar cualquier otro tipo de error
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
