from flask import Flask, render_template, request
from Backend.CourseRecommendation import get_recommendation
import os
import json
import sys

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input = request.form.get('input')
        result = get_recommendation(input)
        return render_template('index.html', result=result, isPost=True)
    else:
        return render_template('index.html', result=None, isPost=False)

'''
def process_score(req, quiz_questions):

    score = 0
    for i, 
'''

Quizzes_folder_path = os.path.join(os.path.dirname(__file__), 'Dataset', 'Quizzes')
    
@app.route('/quiz', methods=['GET', 'POST'])
def show_quiz():
    quiz_path = os.path.join(Quizzes_folder_path, 'python.json')
    with open(quiz_path, 'r') as f:
        quiz_questions = json.load(f)

    if request.method == 'POST': # for form submission
        selected_value = request.form.get(f'question_{1}', default=-1)
        return render_template('quiz.html', selected_value=selected_value)


    
    return render_template('quiz.html', json_content=quiz_questions, selected_value=None)


'''
@app.route('/quiz/submit', methods=['POST'])
def process_quiz():
    selected_value = request.form.get(f'question_{1}', default=-1)
    return render_template('quiz.html', selected_value=selected_value)
'''

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
