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


def process_score(req, quiz_questions):
    '''
    after the user submits the quiz (the user's answers are stored in `req`, the request),
    this function returns the level (basic, intermediate, or advanced) of the user
    '''
    score = 0
    for i, q in enumerate(quiz_questions['questions']):
        selected_value = int(request.form.get(f'question_{i+1}', default=-1))
        if selected_value == q['answer']:
            score += 1

    if score < 3:
        level = 'basic'
    elif score == 3 or score == 4:
        level = 'intermediate'
    else:
        level = 'advanced'

    return level

def process_score1(req, quiz_questions):
    '''
    after the user submits the quiz (the user's answers are stored in req),
    this function returns the score and the answers that the user provided
    '''
    score = 0
    answers = []
    for i, q in enumerate(quiz_questions['questions']):
        selected_value = int(request.form.get(f'question_{i+1}', default=-1))
        answers.append(selected_value)
        if selected_value == q['answer']:
            score += 1
    
    return score, answers


Quizzes_folder_path = os.path.join(os.path.dirname(__file__), 'Dataset', 'Quizzes')
    
@app.route('/quiz', methods=['GET', 'POST'])
def show_quiz():
    quiz_path = os.path.join(Quizzes_folder_path, 'python.json')
    with open(quiz_path, 'r') as f:
        quiz_questions = json.load(f)

    if request.method == 'POST': # for form submission
        user_level = process_score(request, quiz_questions)
        return render_template('quiz.html', json_content=quiz_questions, level=user_level)

    # landing page for /quiz
    return render_template('quiz.html', json_content=quiz_questions, level=None)


'''
@app.route('/quiz/submit', methods=['POST'])
def process_quiz():
    selected_value = request.form.get(f'question_{1}', default=-1)
    return render_template('quiz.html', selected_value=selected_value)
'''

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
