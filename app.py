from flask import Flask, render_template

app = Flask(__name__)

# Define the list of questions and their options
# Replace these questions with the ones you generated
questions = [
    {
        'question': 'What is the output of the following code?',
        'options': ['[1, 2]', '[2, 3]', '[2, 3, 4]', '[1, 2, 3]'],
        'answer': 1,
    },
    # Add other questions here
]

# Define the index to keep track of the current question
current_question_index = 0

# Helper function to get the current question
def get_current_question():
    return questions[current_question_index]

# Helper function to check the user's answer
def check_answer(answer):
    return answer == questions[current_question_index]['answer']

# Define routes for the app
@app.route('/')
def index():
    # render_template will look for `index.html` in the templates folder
    return render_template('index.html', question=get_current_question())

@app.route('/answer/<int:answer>')
def answer(answer):
    is_correct = check_answer(answer)
    return render_template('answer.html', is_correct=is_correct)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
