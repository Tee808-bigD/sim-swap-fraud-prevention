import requests
import json

print("=" * 50)
print("SimGuard API Testing")
print("=" * 50)

# Test 1: Health Check
print("\n1. Testing Health Check...")
try:
    response = requests.get("http://localhost:8000/")
    print(f"✅ Health Check: {response.json()}")
except Exception as e:
    print(f"❌ Health Check Failed: {e}")

# Test 2: Fraud Transaction (Should be BLOCKED)
print("\n2. Testing FRAUD Transaction (SIM Swap + High Value + New Recipient)...")
test_data = {
    "phone_number": "+99999991000",
    "amount": 1000,
    "currency": "KES",
    "recipient": "Fraudster",
    "is_new_recipient": True
}

try:
    response = requests.post(
        "http://localhost:8000/api/transactions",
        json=test_data
    )
    result = response.json()
    print(f"📱 Phone: {result['phone_number']}")
    print(f"💰 Amount: {result['currency']} {result['amount']}")
    print(f"🚦 Status: {result['status']}")
    print(f"📊 Risk Score: {result['risk_score']}")
    print(f"💬 Message: {result['message']}")
    
    if result['status'] == 'blocked':
        print("✅ CORRECT: Fraud transaction was BLOCKED")
    else:
        print("❌ WRONG: Fraud transaction was not blocked")
except Exception as e:
    print(f"❌ Test Failed: {e}")

# Test 3: Normal Transaction (Should be APPROVED)
print("\n3. Testing NORMAL Transaction...")
test_data = {
    "phone_number": "+99999991001",
    "amount": 50,
    "currency": "KES",
    "recipient": "Friend",
    "is_new_recipient": False
}

try:
    response = requests.post(
        "http://localhost:8000/api/transactions",
        json=test_data
    )
    result = response.json()
    print(f"📱 Phone: {result['phone_number']}")
    print(f"💰 Amount: {result['currency']} {result['amount']}")
    print(f"🚦 Status: {result['status']}")
    print(f"📊 Risk Score: {result['risk_score']}")
    print(f"💬 Message: {result['message']}")
    
    if result['status'] == 'approved':
        print("✅ CORRECT: Normal transaction was APPROVED")
    else:
        print("❌ WRONG: Normal transaction was not approved")
except Exception as e:
    print(f"❌ Test Failed: {e}")

# Test 4: Suspicious Transaction (Should be FLAGGED)
print("\n4. Testing SUSPICIOUS Transaction (SIM Swap + Medium Value)...")
test_data = {
    "phone_number": "+99999991000",
    "amount": 300,
    "currency": "KES",
    "recipient": "New Person",
    "is_new_recipient": False
}

try:
    response = requests.post(
        "http://localhost:8000/api/transactions",
        json=test_data
    )
    result = response.json()
    print(f"📱 Phone: {result['phone_number']}")
    print(f"💰 Amount: {result['currency']} {result['amount']}")
    print(f"🚦 Status: {result['status']}")
    print(f"📊 Risk Score: {result['risk_score']}")
    print(f"💬 Message: {result['message']}")
    
    if result['status'] == 'flagged':
        print("✅ CORRECT: Suspicious transaction was FLAGGED")
    else:
        print(f"❌ WRONG: Got {result['status']} instead of flagged")
except Exception as e:
    print(f"❌ Test Failed: {e}")

print("\n" + "=" * 50)
print("Testing Complete!")
print("=" * 50)