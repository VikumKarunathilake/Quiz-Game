import sqlite3

# Connect to your SQLite database (or create it)
conn = sqlite3.connect('quiz.db')
cursor = conn.cursor()

# Create User table
cursor.execute("""
CREATE TABLE IF NOT EXISTS User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL -- Store hashed passwords here!
);
""")

# Create QuizQuestion table
cursor.execute("""
CREATE TABLE IF NOT EXISTS QuizQuestion (
    QuestionID INTEGER PRIMARY KEY AUTOINCREMENT,
    Category TEXT,
    QuestionText TEXT,
    AnswerA TEXT,
    AnswerB TEXT,
    AnswerC TEXT,
    AnswerD TEXT,
    CorrectAnswer TEXT,
    creator_id INTEGER NOT NULL,  -- New field: Foreign Key
    FOREIGN KEY (creator_id) REFERENCES User(id)
);
""")

# Insert quiz questions into the table
questions = [
    ('History', 'Who painted the Mona Lisa?', 'Michelangelo', 'Leonardo da Vinci', 'Raphael', 'Donatello', 'Leonardo da Vinci', 1),
    ('History', 'In what year did World War II begin?', '1914', '1939', '1941', '1945', '1939', 1),
    ('History', 'Who was the first woman to fly solo across the Atlantic Ocean?', 'Amelia Earhart', 'Bessie Coleman', 'Harriet Quimby', 'Jacqueline Cochran', 'Amelia Earhart', 1),
    ('History', 'What ancient civilization built the pyramids?', 'Romans', 'Greeks', 'Egyptians', 'Mayans', 'Egyptians', 1),
    ('History', 'Who wrote the famous play "Hamlet"?', 'William Shakespeare', 'Christopher Marlowe', 'Ben Jonson', 'John Webster', 'William Shakespeare', 1),
    ('Science', 'What is the chemical symbol for gold?', 'Ag', 'Au', 'Fe', 'Hg', 'Au', 1),
    ('Science', 'What is the largest planet in our solar system?', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Jupiter', 1),
    ('Science', 'What is the name of the force that pulls objects towards the center of the Earth?', 'Friction', 'Magnetism', 'Gravity', 'Inertia', 'Gravity', 1),
    ('Science', 'What is the smallest unit of life?', 'Atom', 'Molecule', 'Cell', 'Organ', 'Cell', 1),
    ('Science', 'What is the process by which plants convert sunlight into energy?', 'Respiration', 'Photosynthesis', 'Transpiration', 'Fermentation', 'Photosynthesis', 1),
    ('Geography', 'What is the capital of France?', 'London', 'Berlin', 'Paris', 'Rome', 'Paris', 1),
    ('Geography', 'Which country is the largest in terms of land area?', 'China', 'United States', 'Russia', 'Canada', 'Russia', 1),
    ('Geography', 'What is the longest river in the world?', 'Amazon River', 'Nile River', 'Yangtze River', 'Mississippi River', 'Nile River', 1),
    ('Geography', 'Which ocean is the largest?', 'Atlantic Ocean', 'Indian Ocean', 'Arctic Ocean', 'Pacific Ocean', 'Pacific Ocean', 1),
    ('Geography', 'What is the highest mountain in the world?', 'Mount Kilimanjaro', 'Mount Everest', 'Mount Denali', 'Mount Aconcagua', 'Mount Everest', 1),
    ('Literature', 'Who wrote the Harry Potter series?', 'Stephen King', 'J.K. Rowling', 'George R.R. Martin', 'Suzanne Collins', 'J.K. Rowling', 1),
    ('Literature', 'What is the name of the fictional detective created by Sir Arthur Conan Doyle?', 'Hercule Poirot', 'Miss Marple', 'Sherlock Holmes', 'Philip Marlowe', 'Sherlock Holmes', 1),
    ('Literature', 'Who wrote the novel "Pride and Prejudice"?', 'Jane Austen', 'Charlotte Brontë', 'Emily Brontë', 'Mary Shelley', 'Jane Austen', 1),
    ('Literature', 'What is the name of the famous dystopian novel by George Orwell?', 'Brave New World', 'Fahrenheit 451', 'Nineteen Eighty-Four', 'The Handmaid''s Tale', 'Nineteen Eighty-Four', 1),
    ('Literature', 'Who wrote the epic poem "The Odyssey"?', 'Homer', 'Virgil', 'Ovid', 'Sophocles', 'Homer', 1),
    ('Art', 'What famous artist painted "The Starry Night"?', 'Claude Monet', 'Vincent van Gogh', 'Pablo Picasso', 'Salvador Dalí', 'Vincent van Gogh', 1),
    ('Art', 'What style of art is characterized by bold colors and thick brushstrokes?', 'Impressionism', 'Surrealism', 'Expressionism', 'Cubism', 'Expressionism', 1),
    ('Art', 'What is the name of the famous sculpture by Michelangelo depicting a biblical hero?', 'The Thinker', 'David', 'Venus de Milo', 'The Pieta', 'David', 1),
    ('Art', 'What type of art uses light and shadow to create the illusion of depth?', 'Sculpture', 'Photography', 'Chiaroscuro', 'Pointillism', 'Chiaroscuro', 1),
    ('Art', 'What is the name of the famous prehistoric cave paintings in France?', 'Altamira', 'Lascaux', 'Chauvet', 'Bhimbetka', 'Lascaux', 1),
    ('Music', 'Who is known as the "King of Pop"?', 'Elvis Presley', 'Michael Jackson', 'Prince', 'David Bowie', 'Michael Jackson', 1),
    ('Music', 'What instrument is typically used to play classical music?', 'Electric guitar', 'Violin', 'Saxophone', 'Drums', 'Violin', 1),
    ('Music', 'What genre of music originated in Jamaica?', 'Reggae', 'Blues', 'Jazz', 'Rock and Roll', 'Reggae', 1),
    ('Music', 'Who composed the famous symphony "Moonlight Sonata"?', 'Wolfgang Amadeus Mozart', 'Ludwig van Beethoven', 'Johann Sebastian Bach', 'Franz Schubert', 'Ludwig van Beethoven', 1),
    ('Music', 'What is the name of the musical instrument with black and white keys?', 'Piano', 'Guitar', 'Trumpet', 'Flute', 'Piano', 1),
    ('Sports', 'How many players are on a basketball team?', '5', '6', '7', '8', '5', 1),
    ('Sports', 'What country won the FIFA World Cup in 2018?', 'Brazil', 'Germany', 'France', 'Argentina', 'France', 1),
    ('Sports', 'What is the name of the famous tennis tournament held in Wimbledon, England?', 'US Open', 'French Open', 'Australian Open', 'Wimbledon Championships', 'Wimbledon Championships', 1),
    ('Sports', 'Who is considered the greatest basketball player of all time?', 'LeBron James', 'Michael Jordan', 'Kobe Bryant', 'Kareem Abdul-Jabbar', 'Michael Jordan', 1),
    ('Sports', 'What sport is played with a shuttlecock?', 'Badminton', 'Tennis', 'Squash', 'Volleyball', 'Badminton', 1),
    ('Technology', 'What does "URL" stand for?', 'Universal Resource Locator', 'Uniform Resource Locator', 'Unified Resource Link', 'Universal Resource Link', 'Uniform Resource Locator', 1),
    ('Technology', 'Who invented the World Wide Web?', 'Bill Gates', 'Steve Jobs', 'Tim Berners-Lee', 'Mark Zuckerberg', 'Tim Berners-Lee', 1),
    ('Technology', 'What is the name of the first commercially successful personal computer?', 'Apple II', 'IBM PC', 'Commodore 64', 'Atari 800', 'IBM PC', 1),
    ('Technology', 'What does "CPU" stand for?', 'Central Processing Unit', 'Computer Processing Unit', 'Control Processing Unit', 'Central Program Unit', 'Central Processing Unit', 1),
    ('Technology', 'What is the name of the operating system developed by Google?', 'Windows', 'macOS', 'Linux', 'Android', 'Android', 1),
    ('Food & Drink', 'What country is pizza originally from?', 'Italy', 'Greece', 'Spain', 'France', 'Italy', 1),
    ('Food & Drink', 'What is the main ingredient in guacamole?', 'Tomato', 'Onion', 'Avocado', 'Cilantro', 'Avocado', 1),
    ('Food & Drink', 'What type of alcohol is tequila made from?', 'Grapes', 'Barley', 'Agave', 'Corn', 'Agave', 1),
    ('Food & Drink', 'What is the name of the Japanese dish consisting of vinegared rice topped with seafood and vegetables?', 'Ramen', 'Sushi', 'Tempura', 'Sashimi', 'Sushi', 1),
    ('Food & Drink', 'What is the main ingredient in hummus?', 'Chickpeas', 'Lentils', 'Black beans', 'Kidney beans', 'Chickpeas', 1),
    ('Animals', 'What is the largest land animal?', 'Elephant', 'Giraffe', 'Rhinoceros', 'Hippopotamus', 'Elephant', 1),
    ('Animals', 'What is the fastest land animal?', 'Lion', 'Cheetah', 'Tiger', 'Leopard', 'Cheetah', 1),
    ('Animals', 'What is the name of the largest ocean animal?', 'Great White Shark', 'Blue Whale', 'Giant Squid', 'Orca', 'Blue Whale', 1),
    ('Animals', 'What type of animal is a platypus?', 'Mammal', 'Reptile', 'Amphibian', 'Bird', 'Mammal', 1),
    ('Animals', 'What is the name of the tallest mammal?', 'Giraffe', 'Elephant', 'Zebra', 'Ostrich', 'Giraffe', 1),
    ('Miscellaneous', 'What is the capital of Australia?', 'Sydney', 'Melbourne', 'Canberra', 'Perth', 'Canberra', 1),
    ('Miscellaneous', 'What is the name of the currency used in Japan?', 'Won', 'Yuan', 'Yen', 'Rupee', 'Yen', 1),
    ('Miscellaneous', 'What is the primary language spoken in Brazil?', 'Spanish', 'English', 'Portuguese', 'French', 'Portuguese', 1),
    ('Miscellaneous', 'Who is the author of "The Catcher in the Rye"?', 'J.D. Salinger', 'F. Scott Fitzgerald', 'Ernest Hemingway', 'Mark Twain', 'J.D. Salinger', 1),
    ('Miscellaneous', 'What is the name of the longest river in South America?', 'Nile', 'Amazon', 'Yangtze', 'Mississippi', 'Amazon', 1)
]

# Use executemany to insert multiple questions at once
cursor.executemany("""
INSERT INTO QuizQuestion (Category, QuestionText, AnswerA, AnswerB, AnswerC, AnswerD, CorrectAnswer, creator_id) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
""", questions)

# Commit the changes to the database
conn.commit()

# Close the connection
conn.close()

print("Tables created and data inserted successfully!")
