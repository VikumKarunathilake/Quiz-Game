from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///quiz_app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)

# Import models after db initialization
from models import User, Quiz, Question, Answer, Result
from forms import LoginForm, RegisterForm, QuizForm, QuestionForm

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

def init_db():
    with app.app_context():
        db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def init_db():
    with app.app_context():
        db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html', form=form)
        
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
            app.logger.error(f'Error during registration: {str(e)}')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        quizzes = Quiz.query.filter_by(user_id=current_user.id).all()
        return render_template('dashboard.html', quizzes=quizzes)
    except Exception as e:
        app.logger.error(f'Error accessing dashboard: {str(e)}')
        flash('An error occurred while loading the dashboard.', 'danger')
        return redirect(url_for('home'))

@app.route('/create_quiz', methods=['GET', 'POST'])
@login_required
def create_quiz():
    form = QuizForm()
    if form.validate_on_submit():
        try:
            quiz = Quiz(
                title=form.title.data,
                description=form.description.data,
                user_id=current_user.id
            )
            db.session.add(quiz)
            db.session.commit()
            flash('Quiz created successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error creating quiz: {str(e)}')
            flash('An error occurred while creating the quiz.', 'danger')
    
    return render_template('create_quiz.html', form=form)

@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if request.method == 'POST':
        try:
            # Process quiz submission
            score = 0
            total_questions = len(quiz.questions)
            
            for question in quiz.questions:
                selected_answer_id = request.form.get(f'question_{question.id}')
                if selected_answer_id:
                    selected_answer = Answer.query.get(int(selected_answer_id))
                    if selected_answer and selected_answer.is_correct:
                        score += 1
            
            # Save result
            result = Result(
                score=score,
                user_id=current_user.id,
                quiz_id=quiz.id
            )
            db.session.add(result)
            db.session.commit()
            
            flash(f'Quiz completed! Your score: {score}/{total_questions}', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error processing quiz submission: {str(e)}')
            flash('An error occurred while submitting the quiz.', 'danger')
    
    return render_template('take_quiz.html', quiz=quiz)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)