from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import json
from collections import OrderedDict

app = Flask(__name__)
CORS(app)  # Enable CORS

# Prevent Flask from sorting JSON keys
app.json.sort_keys = False  

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    return n > 0 and sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n):
    if n < 0:
        return False
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

def digit_sum(n):
    return sum(int(d) for d in str(abs(n)))

def get_fun_fact(n):
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math", timeout=5)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return "Fun fact unavailable."
    return "Fun fact unavailable."

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    num_param = request.args.get('number')
    if not num_param or not num_param.lstrip('-').isdigit():
        return jsonify({"number": "alphabet", "error": True}), 400
    
    number = int(num_param)
    properties = ["armstrong"] if is_armstrong(number) else []
    properties.append("even" if number % 2 == 0 else "odd")
    
    # Manually ordering the dictionary
    result = OrderedDict([
        ("number", number),
        ("properties", properties),  # Correctly formatted properties
        ("is_perfect", is_perfect(number)),
        ("is_prime", is_prime(number)),
        ("digit_sum", digit_sum(number)),
        ("fun_fact", get_fun_fact(number))
    ])

    # Return the JSON response directly
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)





