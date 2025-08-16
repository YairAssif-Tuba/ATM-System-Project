# ATM System Server

This is a secure, thread-safe ATM system server built with Flask. The server provides RESTful API endpoints for basic ATM operations including balance checking, deposits, and withdrawals. The system implements account-level locking to prevent race conditions and ensure data integrity during concurrent operations.

## General Approach

The ATM system follows a client-server architecture where the server handles all business logic and data management. The server uses in-memory storage for simplicity and implements thread-safe operations using Python's threading module. Each account has its own lock to prevent concurrent access issues, especially TOCTOU. In addition, each locking try has a timeout of 10 seconds. I was thinking if I should stick with it or not (because then when asking >100 requests in parallel we will face timeout for sure since each operation takes 0.1 second for readability) but I decided to do so since it resembles more to a real banking system.

## Challenges Faced

The most difficult challenge I faced in this assignment was to understand the REST API syntax and how to use it. Although the implementations and the idea of using locks was clear to me, writing the system as a server and not just as a script was something I did not face as a student. However, using AI tools, documentation and reading code, I managed to understand how to write it and I learned a lot from this assignment.

## Features

- **Get Balance**: Retrieve current account balance with account number reference
- **Withdraw Money**: Withdraw specified amount from account (requires existing account)
- **Deposit Money**: Deposit specified amount to account (creates account if it doesn't exist)
- **Thread Safety**: Account-level locking for concurrent access
- **Automatic Account Creation**: New accounts created automatically on first deposit
- **Simple String Responses**: All API responses return human-readable strings

## Pre-loaded Accounts 
- Account: `123456789` - Balance: $1,000.00
- Account: `987654321` - Balance: $2,500.00
- Account: `555555555` - Balance: $500.00

## API Endpoints

### 1. Get Balance
- **URL**: `GET /accounts/{account_number}/balance`
- **Response**: Simple string with account number and balance
- **Example**: `"Account 123456789: Current balance is 1000.0"`

### 2. Withdraw Money
- **URL**: `POST /accounts/{account_number}/withdraw`
- **Request Body**: `{"amount": 100.00}`
- **Success**: `"Account 123456789: Withdrawal successful. New balance is 900.0"`
- **Error**: Returns 404 if account doesn't exist

### 3. Deposit Money
- **URL**: `POST /accounts/{account_number}/deposit`
- **Request Body**: `{"amount": 100.00}`
- **Success**: `"Account 123456789: Deposit successful. New balance is 1100.0"`
- **New Account**: `"Account 123456789: Account created and deposit successful. New balance is 100.0"`

### 4. List All Accounts
- **URL**: `GET /accounts`

## Quick Start

The ATM system server is running and ready to use. You can interact with it using the following methods:

**Live Server**: https://atm-system-project.ew.r.appspot.com

### Test with curl (in cmd, if installed)
```bash
# Get balance
curl -X GET https://atm-system-project.ew.r.appspot.com/accounts/123456789/balance

# Deposit money
curl -X POST https://atm-system-project.ew.r.appspot.com/accounts/123456789/deposit \
-H "Content-Type: application/json" \
-d '{"amount": 100.00}'

# Withdraw money
curl -X POST https://atm-system-project.ew.r.appspot.com/accounts/123456789/withdraw \
-H "Content-Type: application/json" \
-d '{"amount": 50.00}'
```

### Test with Python
```bash
# Run the locking test
python test_locking.py
```

## Security Features

### **Account-Level Locking**
- Each account has its own lock to prevent race conditions
- Only one transaction can access an account at a time
- 10-second timeout prevents deadlocks and allows system to run without waiting too much to lock
- Prevents TOCTOU (Time of Check to Time of Use) vulnerabilities

### **Concurrent Access**
- Multiple users can access different accounts simultaneously
- Same account transactions are serialized for data integrity

## Error Handling
- **404**: Account not found (for withdrawals)
- **400**: Invalid request (missing amount, insufficient balance, negative amounts)
- **423**: Account is busy (locked by another transaction)
- **500**: Server errors

## Testing

```bash
# Run the locking test with random account and thread IDs
python test_locking.py

# Test basic operations manually
curl -X GET https://atm-system-project.ew.r.appspot.com/accounts/123456789/balance
```

## Project Structure

```
ATM System Project/
├── app.py              # Main Flask application with thread safety
├── requirements.txt    # Python dependencies
├── test_locking.py     # Concurrent access testing script
├── app.yaml           # Server configuration
└── README.md          # Project documentation
```

## How to Perform API Calls

### Using curl
```bash
# Get balance
curl -X GET https://atm-system-project.ew.r.appspot.com/accounts/123456789/balance

# Deposit money
curl -X POST https://atm-system-project.ew.r.appspot.com/accounts/123456789/deposit \
-H "Content-Type: application/json" \
-d '{"amount": 200.00}'

# Withdraw money
curl -X POST https://atm-system-project.ew.r.appspot.com/accounts/123456789/withdraw \
-H "Content-Type: application/json" \
-d '{"amount": 100.00}'
```

### Using Python requests
```python
import requests

# Get balance
response = requests.get("https://atm-system-project.ew.r.appspot.com/accounts/123456789/balance")
print(response.text)

# Deposit money
response = requests.post(
    "https://atm-system-project.ew.r.appspot.com/accounts/123456789/deposit",
    json={"amount": 200.00}
)
print(response.text)

# Withdraw money
response = requests.post(
    "https://atm-system-project.ew.r.appspot.com/accounts/123456789/withdraw",
    json={"amount": 100.00}
)
print(response.text)
```


