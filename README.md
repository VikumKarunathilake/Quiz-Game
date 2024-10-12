# Quiz Game

Quiz Game is a web application built with Flask that allows users to take quizzes on various topics. It randomly selects questions from a database and provides instant feedback on the user's performance.

## Features

- Random selection of quiz questions
- User-friendly interface
- Instant score calculation and display
- Responsive design for various devices

## Technologies Used

- Python 3.x
- Flask
- SQLAlchemy
- SQLite
- HTML/CSS
- Bootstrap

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/quiz-game.git
   cd quiz-game
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the environment variables:
   ```
   export SECRET_KEY='your-secret-key'
   ```
   On Windows, use `set` instead of `export`.

5. Initialize the database:
   ```
   flask db upgrade
   ```

6. Run the application:
   ```
   python app.py
   ```

7. Open your web browser and navigate to `http://localhost:5000`.

## Project Structure

- `app.py`: Main application file containing routes and database models
- `templates/`: Directory containing HTML templates
  - `base.html`: Base template with common structure
  - `index.html`: Home page template
  - `quiz.html`: Quiz page template
  - `result.html`: Result page template
- `static/`: Directory for static files (CSS, JS, images)
- `quiz.db`: SQLite database file

## Adding Questions

To add questions to the quiz:

1. Open a Python shell in the project directory
2. Run the following commands:
   ```python
   from app import db, Question
   
   new_question = Question(text="Your question here?", 
                           option1="Option 1", 
                           option2="Option 2", 
                           option3="Option 3", 
                           option4="Option 4", 
                           correct_answer=1)  # 1-4 corresponding to the correct option
   db.session.add(new_question)
   db.session.commit()
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).