from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import random

app = Flask(__name__)
DATABASE = 'quiz.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access data by column name
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_quiz')
def start_quiz():
    conn = get_db_connection()
    questions = conn.execute('SELECT * FROM QuizQuestions ORDER BY RANDOM() LIMIT 10').fetchall()
    conn.close()
    return render_template('quiz.html', questions=questions)

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    score = 0
    if request.method == 'POST':
        answers = request.form
        conn = get_db_connection()
        for question_id, user_answer in answers.items():
            correct_answer = conn.execute('SELECT CorrectAnswer FROM QuizQuestions WHERE QuestionID = ?', (question_id,)).fetchone()[0]
            if user_answer == correct_answer:
                score += 1
        conn.close()
    return render_template('score.html', score=score)


@app.route('/create_quiz')
def create_quiz():
    return render_template('createQuiz.html')

@app.route('/set_username', methods=['POST'])
def set_username():
    if request.method == 'POST':
        session['username'] = request.form['username'] #Store username in the session
    return redirect(url_for('create_quiz'))

@app.route('/save_quiz', methods=['POST'])
def save_quiz():
    if request.method == 'POST':
        category = request.form['category']
        question_text = request.form['questionText']
        answer_a = request.form['answerA']
        answer_b = request.form['answerB']
        answer_c = request.form['answerC']
        answer_d = request.form['answerD']
        correct_answer = request.form['correctAnswer']

        username = session['username']

        conn = get_db_connection()
        conn.execute('INSERT INTO QuizQuestions (Category, QuestionText, AnswerA, AnswerB, AnswerC, AnswerD, CorrectAnswer) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (category, question_text, answer_a, answer_b, answer_c, answer_d, correct_answer))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))



if __name__ == '__main__':
    # Ensure the database exists and has the correct table structure.
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS QuizQuestions (
            QuestionID INTEGER PRIMARY KEY AUTOINCREMENT,
            Category TEXT,
            QuestionText TEXT,
            AnswerA TEXT,
            AnswerB TEXT,
            AnswerC TEXT,
            AnswerD TEXT,
            CorrectAnswer TEXT
        )
    ''')
    conn.close()

    app.run(debug=True)