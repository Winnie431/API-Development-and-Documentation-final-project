## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "resouirce not found"
    
}
```
The API will return Four error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
-405: Method not allowed

### Endpoints 
#### GET /books
- General:
    - Returns a list of categories objects, success value
    - Results are paginated (like in the case  of questions) in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/categories`

``` {
    "categories": [
        {
            "id": 1,
            "type": " Science"
        },
        {
            "id": 2,
            "type": " Art"
        },
        {
            "id": 3,
            "type": " Geography"
        },
        {
            "id": 4,
            "type": " History"
        },
        {
            "id": 5,
            "type": " Entertainment"
        },
        {
            "id": 6,
            "type": " Sport"
        }
    ],
    "success": true
}
```

#### POST /question
- General:
    - Creates a new question using the submitted question, answer,difficulty and category. Returns the id of the created question, success value, total questions, and question list based on current page number to update the frontend. 
- `curl http://127.0.0.1:5000/questions?page=2 -X POST -H "Content-Type: application/json" -d '{"question": "What does the Acronym HTTP Stand for?", "answer": "hypertest Transfer Protocol", 
        "difficulty":4,"category": "Science"}'`
```
{
 "questions": [
        {
            "answer": "Apollo 13",
            "category": "5",
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "success",
            "category": "science",
            "difficulty": 2,
            "id": 3,
            "question": "What is the HTTP Code 200 Indicate??"
        },
        {
            "answer": "Tom Cruise",
            "category": "5",
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Maya Angelou",
            "category": "4",
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled I Know Why the Caged Bird Sings"
        },
        {
            "answer": "Edward Scissorhands",
            "category": "5",
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "HTTP",
            "category": "4",
            "difficulty": 3,
            "id": 7,
            "question": "What is the protocol used in REST?"
        },
        {
            "answer": " Representational State Transfer",
            "category": "4",
            "difficulty": 3,
            "id": 8,
            "question": "What does the Acronym REST Stand for?"
        },
        {
            "answer": "Muhammad Ali",
            "category": "4",
            "difficulty": 1,
            "id": 9,
            "question": "What boxers original name is Cassius Clay?"
        },
        {
            "answer": "Brazil",
            "category": "6",
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": "6",
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        }
    ],
    "success": true,
    "total_questions": 38
}
```
#### DELETE /question/{question_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value, total questions, and questions list based on current page number to update the frontend. 
- `curl -X DELETE http://127.0.0.1:5000/books/16?page=2`
```
{
 "questions": [
        {
            "answer": "Apollo 13",
            "category": "5",
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "success",
            "category": "science",
            "difficulty": 2,
            "id": 3,
            "question": "What is the HTTP Code 200 Indicate??"
        },
        {
            "answer": "Tom Cruise",
            "category": "5",
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Maya Angelou",
            "category": "4",
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled I Know Why the Caged Bird Sings"
        },
        {
            "answer": "Edward Scissorhands",
            "category": "5",
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "HTTP",
            "category": "4",
            "difficulty": 3,
            "id": 7,
            "question": "What is the protocol used in REST?"
        },
        {
            "answer": " Representational State Transfer",
            "category": "4",
            "difficulty": 3,
            "id": 8,
            "question": "What does the Acronym REST Stand for?"
        },
        {
            "answer": "Muhammad Ali",
            "category": "4",
            "difficulty": 1,
            "id": 9,
            "question": "What boxers original name is Cassius Clay?"
        },
        {
            "answer": "Brazil",
            "category": "6",
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": "6",
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        }
    ],
                    "success": True,
                    "deleted": 1,
                    "total_questions": 38,
                   
}
