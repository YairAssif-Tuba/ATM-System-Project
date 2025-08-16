import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:5000"

def test_api():
    """Test all API endpoints"""
    print("🧪 Testing ATM System API...\n")
    
    # Test 1: Get server info
    print("1. Testing server info...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Test 2: List all accounts
    print("2. Testing list accounts...")
    try:
        response = requests.get(f"{BASE_URL}/accounts")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Test 3: Get balance
    print("3. Testing get balance...")
    try:
        response = requests.get(f"{BASE_URL}/accounts/123456789/balance")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Test 4: Deposit money
    print("4. Testing deposit...")
    try:
        deposit_data = {"amount": 100.00}
        response = requests.post(
            f"{BASE_URL}/accounts/123456789/deposit",
            json=deposit_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Test 5: Withdraw money
    print("5. Testing withdraw...")
    try:
        withdraw_data = {"amount": 50.00}
        response = requests.post(
            f"{BASE_URL}/accounts/123456789/withdraw",
            json=withdraw_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Test 6: Get balance after transactions
    print("6. Testing get balance after transactions...")
    try:
        response = requests.get(f"{BASE_URL}/accounts/123456789/balance")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Test 7: Test invalid account
    print("7. Testing invalid account...")
    try:
        response = requests.get(f"{BASE_URL}/accounts/999999999/balance")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Test 8: Test insufficient balance
    print("8. Testing insufficient balance...")
    try:
        withdraw_data = {"amount": 10000.00}
        response = requests.post(
            f"{BASE_URL}/accounts/123456789/withdraw",
            json=withdraw_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    print("✅ API testing completed!")

if __name__ == "__main__":
    test_api()
