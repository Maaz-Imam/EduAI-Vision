import openai
import os
from elevenlabs import generate
from flask import jsonify,request,app, Flask, render_template
import base64
from CourseRecommendation import *

openai_api_key = os.environ.get("OPENAI_API_KEY")
# openai.api_key = ""
elevenlabs_api_key = os.environ.get("ELEVENLABS_API_KEY")

def generate_speech(message,id,flag=0):
    audio = generate(
        text=message,
        voice="Bella",
        model='eleven_monolingual_v1'
    )

    print("\n",message,"\n")

    audio_base64 = base64.b64encode(audio).decode('utf-8')

    data = {
        'audio' : audio_base64,
        'message': message,
        'flag': flag,
        'id': id
    }

    return jsonify(data)



def generate_questions(message):
    messages = [
        {"role": "system", "content": "Generate 3 short theoretical questions to evaluate the user's skills and knowledge in this field."},
        {"role": "user", "content": f"User Input: {message}"}
    ]

    # Make an API call to GPT-3.5 to generate evaluation questions
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        max_tokens=250
    )
    # Extract the generated questions from the API response
    assistant_response = response.choices[0].message['content']
    generated_questions = assistant_response.split("\n")
    generated_questions = [q.strip() for q in generated_questions if q.strip()]

    print(generated_questions,"\n",len(generated_questions))
    return generated_questions

def eval_answer(evaluation_questions,ans_list):
    messages = [
        {"role": "system", "content": "Based on the set of questions and their corresponding answers, generate a phrase of 2-3 words consisting of the user's level (beginner or intermediate or expert) and specifically what field their interest is in. such as 'Beginner Python'"},
        {"role": "user", "content": f"Questions: {evaluation_questions}, Anwers: {ans_list}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        max_tokens=50
    )
    # Extract the generated questions from the API response
    assistant_response = response.choices[0].message['content']
    eval_phrase = assistant_response.split("\n")
    eval_phrase = [q.strip() for q in eval_phrase if q.strip()]

    print(eval_phrase,"\n",len(eval_phrase))
    return str(eval_phrase[0])


ans_list = []
evaluation_questions = []


app = Flask(__name__,template_folder="templates")

@app.route("/", methods=['GET'])
def default():
    return render_template("index.html")

@app.route("/getQues", methods=['POST','GET'])
def question_generator():
    global evaluation_questions
    data = request.get_json()
    message = "No answer provided"
    data = dict(data)
    message = data['message']
    flag = int(data['flag'])
    i = int(data['i'])
        

    if flag==1:
        i=0
        # print("\nI am here\n")
        evaluation_questions = generate_questions(message)
    else: 
        # print("\nI am NOT here\n")
        ans_list.append(message)

    if i>2:
        # print("\n",evaluation_questions,"\n",len(evaluation_questions),"\n")
        # print("\n",ans_list,"\n",len(ans_list),"\n")
        msg = courseRecommender(eval_answer(evaluation_questions,ans_list))
        return generate_speech(msg,i,1)
    else:
        msg = evaluation_questions[i]
        return generate_speech(msg,i)

if __name__ == '__main__':
    app.run()