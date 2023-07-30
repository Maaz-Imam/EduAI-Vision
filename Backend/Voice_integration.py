from elevenlabs import generate, set_api_key
from flask import Response,request,app, Flask, render_template

set_api_key("<enter your key>")

app = Flask(__name__,template_folder="templates")

@app.route("/", methods=['GET'])
def default():
    return render_template("index.html")

@app.route('/talk', methods=['POST','GET'])
def generate_speech():
    data = request.get_json()
    message = data.get('message', 'No message provided')

    audio = generate(
        text=message,
        voice="Bella",
        model='eleven_monolingual_v1'
    )

    return Response(audio, mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run()