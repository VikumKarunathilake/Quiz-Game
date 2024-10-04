import sqlite3
conn = sqlite3.connect('quiz.db')

cursor = conn.cursor()

cursor.execute("""
-- Create the table to store quiz questions
CREATE TABLE QuizQuestions (
    QuestionID INT PRIMARY KEY AUTO_INCREMENT,
    Category VARCHAR(255),
    QuestionText TEXT,
    AnswerA VARCHAR(255),
    AnswerB VARCHAR(255),
    AnswerC VARCHAR(255),
    AnswerD VARCHAR(255),
    CorrectAnswer VARCHAR(255)
);
-- Insert the quiz questions into the table
INSERT INTO QuizQuestions (Category, QuestionText, AnswerA, AnswerB, AnswerC, AnswerD, CorrectAnswer) VALUES
    ('History', 'Who painted the Mona Lisa?', 'Michelangelo', 'Leonardo da Vinci', 'Raphael', 'Donatello', 'Leonardo da Vinci'),
    ('History', 'In what year did World War II begin?', '1914', '1939', '1941', '1945', '1939'),
    ('History', 'Who was the first woman to fly solo across the Atlantic Ocean?', 'Amelia Earhart', 'Bessie Coleman', 'Harriet Quimby', 'Jacqueline Cochran', 'Amelia Earhart'),
    ('History', 'What ancient civilization built the pyramids?', 'Romans', 'Greeks', 'Egyptians', 'Mayans', 'Egyptians'),
    ('History', 'Who wrote the famous play "Hamlet"?', 'William Shakespeare', 'Christopher Marlowe', 'Ben Jonson', 'John Webster', 'William Shakespeare'),
    ('Science', 'What is the chemical symbol for gold?', 'Ag', 'Au', 'Fe', 'Hg', 'Au'),
    ('Science', 'What is the largest planet in our solar system?', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Jupiter'),
    ('Science', 'What is the name of the force that pulls objects towards the center of the Earth?', 'Friction', 'Magnetism', 'Gravity', 'Inertia', 'Gravity'),
    ('Science', 'What is the smallest unit of life?', 'Atom', 'Molecule', 'Cell', 'Organ', 'Cell'),
    ('Science', 'What is the process by which plants convert sunlight into energy?', 'Respiration', 'Photosynthesis', 'Transpiration', 'Fermentation', 'Photosynthesis'),
    ('Geography', 'What is the capital of France?', 'London', 'Berlin', 'Paris', 'Rome', 'Paris'),
    ('Geography', 'Which country is the largest in terms of land area?', 'China', 'United States', 'Russia', 'Canada', 'Russia'),
    ('Geography', 'What is the longest river in the world?', 'Amazon River', 'Nile River', 'Yangtze River', 'Mississippi River', 'Nile River'),
    ('Geography', 'Which ocean is the largest?', 'Atlantic Ocean', 'Indian Ocean', 'Arctic Ocean', 'Pacific Ocean', 'Pacific Ocean'),
    ('Geography', 'What is the highest mountain in the world?', 'Mount Kilimanjaro', 'Mount Everest', 'Mount Denali', 'Mount Aconcagua', 'Mount Everest'),
    ('Literature', 'Who wrote the Harry Potter series?', 'Stephen King', 'J.K. Rowling', 'George R.R. Martin', 'Suzanne Collins', 'J.K. Rowling'),
    ('Literature', 'What is the name of the fictional detective created by Sir Arthur Conan Doyle?', 'Hercule Poirot', 'Miss Marple', 'Sherlock Holmes', 'Philip Marlowe', 'Sherlock Holmes'),
    ('Literature', 'Who wrote the novel "Pride and Prejudice"?', 'Jane Austen', 'Charlotte Brontë', 'Emily Brontë', 'Mary Shelley', 'Jane Austen'),
    ('Literature', 'What is the name of the famous dystopian novel by George Orwell?', 'Brave New World', 'Fahrenheit 451', 'Nineteen Eighty-Four', 'The Handmaid''s Tale', 'Nineteen Eighty-Four'),
    ('Literature', 'Who wrote the epic poem "The Odyssey"?', 'Homer', 'Virgil', 'Ovid', 'Sophocles', 'Homer'),
    ('Art', 'What famous artist painted "The Starry Night"?', 'Claude Monet', 'Vincent van Gogh', 'Pablo Picasso', 'Salvador Dalí', 'Vincent van Gogh'),
    ('Art', 'What style of art is characterized by bold colors and thick brushstrokes?', 'Impressionism', 'Surrealism', 'Expressionism', 'Cubism', 'Expressionism'),
    ('Art', 'What is the name of the famous sculpture by Michelangelo depicting a biblical hero?', 'The Thinker', 'David', 'Venus de Milo', 'The Pieta', 'David'),
    ('Art', 'What type of art uses light and shadow to create the illusion of depth?', 'Sculpture', 'Photography', 'Chiaroscuro', 'Pointillism', 'Chiaroscuro'),
    ('Art', 'What is the name of the famous prehistoric cave paintings in France?', 'Altamira', 'Lascaux', 'Chauvet', 'Bhimbetka', 'Lascaux'),
    ('Music', 'Who is known as the "King of Pop"?', 'Elvis Presley', 'Michael Jackson', 'Prince', 'David Bowie', 'Michael Jackson'),
    ('Music', 'What instrument is typically used to play classical music?', 'Electric guitar', 'Violin', 'Saxophone', 'Drums', 'Violin'),
    ('Music', 'What genre of music originated in Jamaica?', 'Reggae', 'Blues', 'Jazz', 'Rock and Roll', 'Reggae'),
    ('Music', 'Who composed the famous symphony "Moonlight Sonata"?', 'Wolfgang Amadeus Mozart', 'Ludwig van Beethoven', 'Johann Sebastian Bach', 'Franz Schubert', 'Ludwig van Beethoven'),
    ('Music', 'What is the name of the musical instrument with black and white keys?', 'Piano', 'Guitar', 'Trumpet', 'Flute', 'Piano'),
    ('Sports', 'How many players are on a basketball team?', '5', '6', '7', '8', '5'),
    ('Sports', 'What country won the FIFA World Cup in 2018?', 'Brazil', 'Germany', 'France', 'Argentina', 'France'),
    ('Sports', 'What is the name of the famous tennis tournament held in Wimbledon, England?', 'US Open', 'French Open', 'Australian Open', 'Wimbledon Championships', 'Wimbledon Championships'),
    ('Sports', 'Who is considered the greatest basketball player of all time?', 'LeBron James', 'Michael Jordan', 'Kobe Bryant', 'Kareem Abdul-Jabbar', 'Michael Jordan'),
    ('Sports', 'What sport is played with a shuttlecock?', 'Badminton', 'Tennis', 'Squash', 'Volleyball', 'Badminton'),
    ('Technology', 'What does "URL" stand for?', 'Universal Resource Locator', 'Uniform Resource Locator', 'Unified Resource Link', 'Universal Resource Link', 'Uniform Resource Locator'),
    ('Technology', 'Who invented the World Wide Web?', 'Bill Gates', 'Steve Jobs', 'Tim Berners-Lee', 'Mark Zuckerberg', 'Tim Berners-Lee'),
    ('Technology', 'What is the name of the first commercially successful personal computer?', 'Apple II', 'IBM PC', 'Commodore 64', 'Atari 800', 'IBM PC'),
    ('Technology', 'What does "CPU" stand for?', 'Central Processing Unit', 'Computer Processing Unit', 'Control Processing Unit', 'Central Program Unit', 'Central Processing Unit'),
    ('Technology', 'What is the name of the operating system developed by Google?', 'Windows', 'macOS', 'Linux', 'Android', 'Android'),
    ('Food & Drink', 'What country is pizza originally from?', 'Italy', 'Greece', 'Spain', 'France', 'Italy'),
    ('Food & Drink', 'What is the main ingredient in guacamole?', 'Tomato', 'Onion', 'Avocado', 'Cilantro', 'Avocado'),
    ('Food & Drink', 'What type of alcohol is tequila made from?', 'Grapes', 'Barley', 'Agave', 'Corn', 'Agave'),
    ('Food & Drink', 'What is the name of the Japanese dish consisting of vinegared rice topped with seafood and vegetables?', 'Ramen', 'Sushi', 'Tempura', 'Sashimi', 'Sushi'),
    ('Food & Drink', 'What is the main ingredient in hummus?', 'Chickpeas', 'Lentils', 'Black beans', 'Kidney beans', 'Chickpeas'),
    ('Animals', 'What is the largest land animal?', 'Elephant', 'Giraffe', 'Rhinoceros', 'Hippopotamus', 'Elephant'),
    ('Animals', 'What is the fastest land animal?', 'Lion', 'Cheetah', 'Tiger', 'Leopard', 'Cheetah'),
    ('Animals', 'What is the name of the largest ocean animal?', 'Great White Shark', 'Blue Whale', 'Giant Squid', 'Orca', 'Blue Whale'),
    ('Animals', 'What type of animal is a platypus?', 'Mammal', 'Reptile', 'Amphibian', 'Bird', 'Mammal'),
    ('Animals', 'What is the name of the tallest mammal?', 'Giraffe', 'Elephant', 'Zebra', 'Ostrich', 'Giraffe'),
    ('Miscellaneous', 'What is the capital of Australia?', 'Sydney', 'Melbourne', 'Canberra', 'Perth', 'Canberra'),
    ('Miscellaneous', 'What is the name of the currency used in Japan?', 'Won', 'Yuan', 'Yen', 'Rupee', 'Yen'),
    ('Miscellaneous', 'What is the primary language spoken in Brazil?', 'Spanish', 'English', 'Portuguese', 'French', 'Portuguese'),
    ('Miscellaneous', 'Who is the author of "The Catcher in the Rye"?', 'J.D. Salinger', 'F. Scott Fitzgerald', 'Ernest Hemingway', 'Mark Twain', 'J.D. Salinger'),
    ('Miscellaneous', 'What is the name of the longest river in South America?', 'Nile', 'Amazon', 'Yangtze', 'Mississippi', 'Amazon');
""")

# Commit the changes to the database
conn.commit()

# Close the connection
conn.close()

print("Table 'QuizQuestions' created successfully!")