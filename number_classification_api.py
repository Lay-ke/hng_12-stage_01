# from fastapi import FastAPI, Query, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from typing import Union
# import requests

# app = FastAPI()

# def is_prime(n: int) -> bool:
#     if n < 2:
#         return False
#     for i in range(2, int(n ** 0.5) + 1):
#         if n % i == 0:
#             return False
#     return True

# def is_perfect(n: int) -> bool:
#     return n > 0 and sum(i for i in range(1, n) if n % i == 0) == n

# def is_armstrong(n: int) -> bool:
#     digits = [int(d) for d in str(n)]
#     return sum(d ** len(digits) for d in digits) == n

# def get_fun_fact(n: int) -> str:
#     try:
#         response = requests.get(f"http://numbersapi.com/{n}/math")
#         if response.status_code == 200:
#             return response.text
#     except requests.RequestException:
#         return f"Could not retrieve a fun fact for {n}."
#     return f"No fun fact available for {n}."

# def classify_number(n: int):
#     properties = ["odd" if n % 2 != 0 else "even"]
#     if is_armstrong(n):
#         properties.append("armstrong")
    
#     return {
#         "number": n,
#         "is_prime": is_prime(n),
#         "is_perfect": is_perfect(n),
#         "properties": properties,
#         "digit_sum": sum(map(int, str(n))),
#         "fun_fact": get_fun_fact(n)
#     }

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the number classification API!"}

# @app.get("/api/classify-number")
# def get_number_properties(number: str = Query(..., description="An integer to classify")):
#     if not number.isdigit() and not (number.startswith("-") and number[1:].isdigit()):
#         raise HTTPException(status_code=400, detail={"number": number, "error": True})
    
#     number = int(number)
#     return classify_number(number)

from fastapi import FastAPI, Query, HTTPException
from typing import Union
import requests

app = FastAPI()

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    return n > 0 and sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(abs(n))]
    return sum(d ** len(digits) for d in digits) == abs(n)

def get_fun_fact(n: int) -> str:
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math", timeout=5)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return f"Could not retrieve a fun fact for {n}."
    return f"No fun fact available for {n}."

def classify_number(n: Union[int, float]):
    properties = ["odd" if int(n) % 2 != 0 else "even"]
    if is_armstrong(int(n)):
        properties.append("armstrong")
    if isinstance(n, int) and is_prime(n):
        properties.append("prime")
    if isinstance(n, int) and is_perfect(n):
        properties.append("perfect")
    
    return {
        "number": n,
        "is_prime": is_prime(n) if isinstance(n, int) else False,
        "is_perfect": is_perfect(n) if isinstance(n, int) else False,
        "properties": properties,
        "digit_sum": sum(map(int, str(abs(int(n))))),
        "fun_fact": get_fun_fact(int(n))
    }

@app.get("/api/classify-number", response_model=dict)
def get_number_properties(number: str = Query(..., description="A number to classify")):
    try:
        if "." in number:
            number = float(number)
        else:
            number = int(number)
    except ValueError:
        raise HTTPException(status_code=400, detail={"number": str(number), "error": True})
    
    return classify_number(number)