from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.sql.expression import func

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    option1 = db.Column(db.String(100), nullable=False)
    option2 = db.Column(db.String(100), nullable=False)
    option3 = db.Column(db.String(100), nullable=False)
    option4 = db.Column(db.String(100), nullable=False)
    correct_answer = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        # Process the quiz answers and calculate the score
        score = 0
        # Retrieve the 10 random questions stored in the session
        question_ids = session.get('questions')
        if question_ids:
            questions = Question.query.filter(Question.id.in_(question_ids)).all()
            for question in questions:
                user_answer = request.form.get(f'question_{question.id}')
                if user_answer and int(user_answer) == question.correct_answer:
                    score += 1
            return redirect(url_for('result', score=score, total=len(questions)))
    
    # Fetch 10 random questions and store their IDs in the session
    questions = Question.query.order_by(func.random()).limit(10).all()
    session['questions'] = [question.id for question in questions]
    
    return render_template('quiz.html', questions=questions)

@app.route('/result/<int:score>/<int:total>')
def result(score, total):
    return render_template('result.html', score=score, total=total)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
