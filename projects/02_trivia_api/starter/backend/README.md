# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

Endpoints:

- GET `/categories`
- GET `/questions`
- GET `/categories/<int:category_id>/questions`
- DELETE `/questions/<int:question_id>`
- POST `/questions`
- POST `/questions/search`
- POST `/quizzes`

---

GET `/categories`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.

```

{
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"
}

```

---

GET `/questions`

- Fetches a dictionary of paginated questions (10 qestions per page).
- Request Arguments: None
- Returns: An object with the following keys: categories, current_category, questions,success and total questions.

```

{
categories: {
    1: "Science",
    2: "Art",
    3: "Geography",
    4: "History",
    5: "Entertainment",
    6: "Sports"
},
current_category: null,
questions: [
    {
    answer: "Brazil",
    category: 6,
    difficulty: 3,
    id: 10,
    question: "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
    answer: "Uruguay",
    category: 6,
    difficulty: 4,
    id: 11,
    question: "Which country won the first ever soccer World Cup in 1930?"
    },
    {
    answer: "George Washington Carver",
    category: 4,
    difficulty: 2,
    id: 12,
    question: "Who invented Peanut Butter?"
    },
    {
    answer: "The Palace of Versailles",
    category: 3,
    difficulty: 3,
    id: 14,
    question: "In which royal palace would you find the Hall of Mirrors?"
    },
    {
    answer: "Agra",
    category: 3,
    difficulty: 2,
    id: 15,
    question: "The Taj Mahal is located in which Indian city?"
    },
    {
    answer: "Escher",
    category: 2,
    difficulty: 1,
    id: 16,
    question: "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    },
    {
    answer: "One",
    category: 2,
    difficulty: 4,
    id: 18,
    question: "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
    answer: "Jackson Pollock",
    category: 2,
    difficulty: 2,
    id: 19,
    question: "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
    answer: "Alexander Fleming",
    category: 1,
    difficulty: 3,
    id: 21,
    question: "Who discovered penicillin?"
    },
    {
    answer: "Blood",
    category: 1,
    difficulty: 4,
    id: 22,
    question: "Hematology is a branch of medicine involving the study of what?"
    }
],
success: true,
total_questions: 35
}

```

---

GET `/categories/1/questions`

- Fetches questions for a chosen category
- Request Arguments: Category Id - as part of the url
- Returns: success key as the outcome of the search, total questions found, questions temselves and the category chosen as the current category.

```

{
    'success': true,
    'questions': [
        {
        answer: "Blood",
        category: 1,
        difficulty: 4,
        id: 22,
        question: "Hematology is a branch of medicine involving the study of what?"
        }
    ],
    'total_questions': 1,
    'current_category': 1
}

```

---

DELETE `/questions/1`

- Deletes a question with a specific ID
- Request Arguments: question_id - part of the url
- Returns: success key as the outcome of the delete and deleted question's id.

```

{
    "success": true,
    "deleted_id": 1
}

```

---

POST `/questions`

```
{
    'question': 'How old am I?',
    'answer': '27',
    'difficuty': 1,
    'category': 1
}
```

- Creates a new question
- Request Arguments: and object with a question, answer, difficulty and category
- Returns: success key as the outcome of the search and a message confirming the success

```

{
    'success': true,
    'message': 'Question has been added successfully'
}

```

---

POST `/questions/search`

```
{
    'searchTerm': 'Hematology'
}
```

- Fetches questions that match your search term
- Request Arguments: search term, passed as a json key with a string value
- Returns: success key as the outcome of the search, total questions found, questions temselves and the current category

```

{
    'success': True,
    'total_questions': 1,
    'questions': [
        {
        answer: "Blood",
        category: 1,
        difficulty: 4,
        id: 22,
        question: "Hematology is a branch of medicine involving the study of what?"
        }
    ],
    'current_category': null
}

```

---

POST `/quizzes`

```
{
    'previous_questions': [],
    'quiz_category':
        {
        'type': 'Science',
        'id': '1'
        }
}
```

- Fetches a random question for a particular category that hasn't been asked yet
- Request Arguments: a list of previous question ids and a request category object with the name and the id of a category chosen (for all categories pass the id 0)
- Returns: success key as the outcome of the search and the random question object

```

{
    'success': true,
    'question':
        {
        answer: "Blood",
        category: 1,
        difficulty: 4,
        id: 22,
        question: "Hematology is a branch of medicine involving the study of what?"
        }
}

```

---

Error Handlers:

- 503
- 422
- 404

503 `Service Unavailable`

- Fetched when the connectivity to the database is not working.
- Application: applicable to all CRUD operations

```
{
    'success': false,
    'error': 503,
    'message': ':-( Issue communicating with the database :-('
}
```

422 `Unprocessable Entity`

- Fetched when the processing can not be completed due to the input of the request.
- Application: applicable to requests with non existant resource (for example: finding questions for categories that do not exist)

```
{
      'success': false,
      'error': 422,
      'message': 'Unprocessable'
}
```

404 `Not Found`

- Fetched when the resource requested does not exist
- Application: applicable to requests for specific entities (page, category that do not exist)

```
{
      'success': false,
      'error': 404,
      'message': 'Resource does not exist'
}
```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
