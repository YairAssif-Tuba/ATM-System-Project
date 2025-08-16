from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time

app = Flask(__name__)
CORS(app)

# In-memory storage with account-level locks
accounts = {
    "123456789": {"account_number": "123456789", "balance": 1000.00},
    "987654321": {"account_number": "987654321", "balance": 2500.00},
    "555555555": {"account_number": "555555555", "balance": 500.00}
}

# Account-level locks to prevent TOCTOU errors
account_locks = {}
lock_creation_lock = threading.Lock()  # Lock for creating account locks

def get_or_create_account_lock(account_number):
    """Get or create a lock for a specific account"""
    if account_number not in account_locks:
        with lock_creation_lock:
            if account_number not in account_locks:
                account_locks[account_number] = threading.Lock()
    return account_locks[account_number]

@app.route('/')
def home():
    return jsonify({
        "message": "ATM System Server with In-Memory Storage and Locks",
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
    lock = get_or_create_account_lock(account_number)
    
    # Acquire lock to ensure consistent read
    if not lock.acquire(timeout=20):
        return f"Account {account_number} is busy, please try again later", 423
    
    try:
        if account_number not in accounts:
            return f"Account {account_number} not found", 404
        
        balance = accounts[account_number]["balance"]
        return f"Account {account_number}: Current balance is {balance}"
    
    finally:
        lock.release()

@app.route('/accounts/<account_number>/withdraw', methods=['POST'])
def withdraw(account_number):
    """Withdraw money from an account. This operation WILL NOT create an account if it doesn't exist."""
    data = request.get_json()
    if not data or 'amount' not in data:
        return f"Account {account_number}: Amount is required", 400
    amount = data['amount']
    
    # Validate amount
    try:
        amount = float(amount)
        if amount <= 0:
            return f"Account {account_number}: Amount must be positive", 400
    except (ValueError, TypeError):
        return f"Account {account_number}: Invalid amount format", 400
    
    lock = get_or_create_account_lock(account_number)
    
    # Try to acquire the lock with timeout
    if not lock.acquire(timeout=20):
        return f"Account {account_number} is busy, please try again later", 423
    
    try:
        # Check if account exists
        if account_number not in accounts:
            return f"Account {account_number} not found", 404
        
        # Get current balance
        current_balance = accounts[account_number]["balance"]
        
        # Check if sufficient balance
        if current_balance < amount:
            return f"Account {account_number}: Insufficient balance", 400
        
        # Simulate some processing time (like real ATM operations)
        time.sleep(0.1)
        
        # Perform withdrawal atomically (within the lock)
        new_balance = current_balance - amount
        accounts[account_number]["balance"] = new_balance
        
        return f"Account {account_number}: Withdrawal successful. New balance is {new_balance}"
    
    finally:
        # Always release the lock
        lock.release()

@app.route('/accounts/<account_number>/deposit', methods=['POST'])
def deposit(account_number):
    """Deposit money into an account. If account doesn't exist, it will be created."""
    data = request.get_json()
    if not data or 'amount' not in data:
        return f"Account {account_number}: Amount is required", 400
    
    amount = data['amount']

    # Validate amount
    try:
        amount = float(amount)
        if amount <= 0:
            return f"Account {account_number}: Amount must be positive", 400
    except (ValueError, TypeError):
        return f"Account {account_number}: Invalid amount format", 400
    
    lock = get_or_create_account_lock(account_number)
    
    # Try to acquire the lock with timeout
    if not lock.acquire(timeout=20):
        return f"Account {account_number} is busy, please try again later", 423
    
    try:
        # Check if account exists
        account_created = False
        if account_number not in accounts:
            # Create new account
            accounts[account_number] = {"account_number": account_number, "balance": 0.00}
            account_created = True
        
        # Get current balance
        current_balance = accounts[account_number]["balance"]
        
        # Simulate some processing time (like real ATM operations)
        time.sleep(0.1)
        
        # Perform deposit atomically (within the lock)
        new_balance = current_balance + amount
        accounts[account_number]["balance"] = new_balance
        
        # Prepare response message
        if account_created:
            return f"Account {account_number}: Account created and deposit successful. New balance is {new_balance}"
        else:
            return f"Account {account_number}: Deposit successful. New balance is {new_balance}"
    
    finally:
        # Always release the lock
        lock.release()

@app.route('/accounts', methods=['GET'])
def list_accounts():
    """List all accounts (for testing purposes)"""
    return jsonify({
        "accounts": list(accounts.values()),
        "total_accounts": len(accounts)
    })

if __name__ == '__main__':
    print("🚀 Starting ATM System Server with In-Memory Storage and Locks...")
    print("📊 Pre-loaded accounts:")
    for account_number, account in accounts.items():
        print(f"   Account {account_number}: ${account['balance']}")
    print("🔒 Account-level locks enabled to prevent TOCTOU errors")
    app.run(debug=True, host='0.0.0.0', port=5000)


