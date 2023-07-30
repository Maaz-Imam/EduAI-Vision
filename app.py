from flask import Flask, render_template, request
from Backend.CourseRecommendation import get_recommendation

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input = request.form.get('input')
        result = get_recommendation(input)
        return render_template('index.html', result=result, isPost=True)
    else:
        return render_template('index.html', result=None, isPost=False)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
