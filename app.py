from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import random
 
app = Flask(__name__)

# Function to get 10 random questions
def get_random_questions():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    
    # Query to select 10 random quiz questions
    cursor.execute("SELECT * FROM QuizQuestions ORDER BY RANDOM() LIMIT 10")
    questions = cursor.fetchall()
    conn.close()
    return questions

@app.route('/')
def index():
    # Get 10 random questions
    questions = get_random_questions()
    return render_template('index.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    total_questions = 10
    answers = request.form
    
    # Connect to the database to check correct answers
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    for qid, answer in answers.items():
        cursor.execute("SELECT CorrectAnswer FROM QuizQuestions WHERE QuestionID = ?", (qid,))
        correct_answer = cursor.fetchone()[0]

        if answer == correct_answer:
            score += 1
    
    conn.close()
    
    return f"Your score is {score} out of {total_questions}"

if __name__ == '__main__':
    app.run(debug=True)
