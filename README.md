# Numbers API

This is a simple FastAPI-based API that allows you to classify numbers based on several mathematical properties and retrieve fun facts about numbers. It supports checking if a number is prime, perfect, or an Armstrong number, and it also provides a fun fact about the number.

## Features

- **Classify a number**: Check if the number is:
  - Prime
  - Perfect
  - Armstrong
  - Odd or Even
- **Retrieve fun facts**: Get a fun fact about the number from the Numbers API.

## Installation

To get started with this API, follow these steps:

### Requirements

- Python 3.7 or later

### Steps to install:

1. Clone the repository:

   ```
   git clone <repository_url>
   cd <repository_directory>
   ```

2.  Install the required dependencies:

    ```
    pip install fastapi uvicorn requests
    ```

Running the API
---------------

To run the API, use Uvicorn as the ASGI server:
```

uvicorn main:app --host 0.0.0.0 --port 80 --reload
```
This will start the server on `http://0.0.0.0`. You can then interact with the API through the available endpoints.

API Endpoints
-------------

### Root Endpoint

**GET /**

Returns a welcome message.


`{
  "message": "Welcome to the number classification API!"
}`

### Classify a Number

**GET /api/classify-number**

Classify a number and retrieve its properties. This endpoint accepts a query parameter `number` (integer) and returns a JSON response with classification results.

#### Parameters

-   `number` (required): The number to classify.

#### Example Request


`GET http://0.0.0.0/api/classify-number?number=153`

#### Example Response

`{
  "number": 153,
  "is_prime": false,
  "is_perfect": false,
  "properties": [
    "armstrong",
    "odd"
  ],
  "digit_sum": 9,
  "fun_fact": "153 is a narcissistic number."
}`

### Error Handling

If the provided number is invalid, the API will return a 400 error with details:

#### Example Response (Invalid Input)

`{
  "number": "abc",
  "error": true
}`

Functions Used
--------------

-   **is_prime(n: int) -> bool**: Checks if the number is prime.
-   **is_perfect(n: int) -> bool**: Checks if the number is a perfect number.
-   **is_armstrong(n: int) -> bool**: Checks if the number is an Armstrong number.
-   **get_fun_fact(n: int) -> str**: Fetches a fun fact about the number from Numbers API.