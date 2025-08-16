from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time

app = Flask(__name__)
CORS(app)

# In-memory storage for accounts
accounts = {
    "123456789": {"account_number": "123456789", "balance": 1000.00},
    "987654321": {"account_number": "987654321", "balance": 2500.00},
    "555555555": {"account_number": "555555555", "balance": 500.00}
}

# Account locks for thread safety
account_locks = {
    "123456789": threading.Lock(),
    "987654321": threading.Lock(),
    "555555555": threading.Lock()
}

@app.route('/')
def home():
    return jsonify({
        "message": "ATM System Server",
        "status": "running",
        "endpoints": {
            "get_balance": "GET /accounts/{account_number}/balance",
            "withdraw": "POST /accounts/{account_number}/withdraw",
            "deposit": "POST /accounts/{account_number}/deposit",
            "list_accounts": "GET /accounts"
        }
    })

@app.route('/accounts/<account_number>/balance', methods=['GET'])
def get_balance(account_number):
    """Get the current balance of an account"""
    if account_number not in accounts:
        return jsonify({"error": "Account not found"}), 404
    
    account = accounts[account_number]
    
    # Check if simple response is requested
    simple = request.args.get('simple', 'false').lower() == 'true'
    
    if simple:
        # Return just the balance number
        return jsonify(account["balance"])
    else:
        # Return full JSON response
        return jsonify({
            "account_number": account_number,
            "balance": account["balance"],
            "message": "Balance retrieved successfully"
        })

@app.route('/accounts/<account_number>/withdraw', methods=['POST'])
def withdraw(account_number):
    """Withdraw money from an account. This operation WILL NOT create an account if it doesn't exist."""
    if account_number not in accounts:
        return jsonify({"error": "Account not found"}), 404
    
    # Get the lock for this account, error if not found
    if account_number not in account_locks: 
        return jsonify({"error": "Account lock not found"}), 500
    
    lock = account_locks[account_number]
    
    # Try to acquire the lock with timeout. If timeout reached, return error and busy message
    if not lock.acquire(timeout=10):
        return jsonify({"error": "Account is busy, please try again later"}), 423  # 423 = Locked
    
    try:
        data = request.get_json()
        if not data or 'amount' not in data:
            return jsonify({"error": "Amount is required"}), 400
        amount = data['amount']
        
        # Validate amount
        try:
            amount = float(amount)
            if amount <= 0: # No minuses in our ATM
                return jsonify({"error": "Amount must be positive"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid amount format"}), 400
        
        account = accounts[account_number]
        
        # Check if sufficient balance
        if account["balance"] < amount: #Cannot withdraw more than you have
            return jsonify({"error": "Insufficient balance"}), 400
        
        # Simulate some processing time (like real ATM operations)
        time.sleep(0.1)
        
        # Perform withdrawal (Everything that needs to be locked is locked)
        account["balance"] -= amount
        
        return jsonify({
            "account_number": account_number,
            "withdrawn_amount": amount,
            "new_balance": account["balance"],
            "message": "Withdrawal successful"
        })
    
    finally:
        # Always release the lock (Even if there is an error)
        lock.release()

@app.route('/accounts/<account_number>/deposit', methods=['POST'])
def deposit(account_number):
    """Deposit money into an account. If account doesn't exist, it will be created."""
    # Check if account exists, if not create it
    account_created = False
    if account_number not in accounts:
        # Create new account with 0 balance
        accounts[account_number] = {"account_number": account_number, "balance": 0.00}
        # Create lock for new account
        account_locks[account_number] = threading.Lock()
        account_created = True
    
    # Get the lock for this account
    lock = account_locks[account_number]
    
    # Try to acquire the lock with timeout
    if not lock.acquire(timeout=10):  # 10 second timeout as same as in withdraw
        return jsonify({"error": "Account is busy, please try again later"}), 423  # 423 = Locked
    
    try:
        data = request.get_json()
        if not data or 'amount' not in data:
            return jsonify({"error": "Amount is required"}), 400
        
        amount = data['amount']

        # Validate amount
        try:
            amount = float(amount)
            if amount <= 0:
                return jsonify({"error": "Amount must be positive"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid amount format"}), 400
        
        account = accounts[account_number]
        
        # Simulate some processing time (like real ATM operations)
        time.sleep(0.1)
        
        # Perform deposit
        account["balance"] += amount
        
        # Prepare response message
        if account_created:
            message = "Account created and deposit successful"
        else:
            message = "Deposit successful"
        
        return jsonify({
            "account_number": account_number,
            "deposited_amount": amount,
            "new_balance": account["balance"],
            "message": message,
            "account_created": account_created
        })
    
    finally:
        # Always release the lock (Even if there is an error)
        lock.release()

@app.route('/accounts', methods=['GET'])
def list_accounts():
    """List all accounts (for testing purposes)"""
    return jsonify({
        "accounts": list(accounts.values()),
        "total_accounts": len(accounts)
    })



if __name__ == '__main__':
    print("Starting ATM System Server...")
    time.sleep(0.5)
    print("Server will be available at: http://localhost:5000")
    time.sleep(0.5)
    print("API Documentation: http://localhost:5000")
    time.sleep(0.5)
    print("Test accounts: 123456789, 987654321, 555555555")
    time.sleep(0.5)
    print("Press Ctrl+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
