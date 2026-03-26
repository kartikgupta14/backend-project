from flask import Flask, jsonify, request
import json
import os

print("App is starting...")

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'data', 'customers.json')

with open(file_path) as f:
    customers = json.load(f)

@app.route('/api/health')
def health():
    return {"status": "ok"}

@app.route('/api/customers')
def get_customers():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    start = (page - 1) * limit
    end = start + limit

    data = customers[start:end]

    return jsonify({
        "data": data,
        "total": len(customers),
        "page": page,
        "limit": limit
    })

@app.route('/api/customers/<customer_id>')
def get_customer(customer_id):
    for customer in customers:
        if customer["customer_id"] == customer_id:
            return jsonify(customer)
    
    return {"error": "Customer not found"}, 404


if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)