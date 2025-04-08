import requests
import json
import time
import os
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

# API URL
API_URL = "https://integration-api-sgo.onrender.com"

# Test credentials
USERNAME = os.getenv("ZUREO_EMAIL", "test@example.com")
PASSWORD = os.getenv("ZUREO_PASSWORD", "password")
TEST_SKU = os.getenv("TEST_SKU", "TEST123")
TEST_QUANTITY = int(os.getenv("TEST_QUANTITY", "10"))

def print_header(text):
    print("\n" + "=" * 50)
    print(f" {text} ".center(50, "="))
    print("=" * 50)

def print_result(test_name, success, response=None, error=None):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} | {test_name}")
    if response:
        print(f"Response: {json.dumps(response, indent=2)}")
    if error:
        print(f"Error: {error}")
    print("-" * 50)

def test_health_check():
    print_header("Testing Health Check Endpoint")
    try:
        response = requests.get(f"{API_URL}/")
        success = response.status_code == 200
        print_result("Health Check", success, response.json() if success else None)
        return success
    except Exception as e:
        print_result("Health Check", False, error=str(e))
        return False

def test_login():
    print_header("Testing Login Endpoint")
    try:
        response = requests.post(
            f"{API_URL}/zureo/login",
            json={"username": USERNAME, "password": PASSWORD}
        )
        success = response.status_code == 200
        print_result("Login", success, response.json() if success else None)
        return success
    except Exception as e:
        print_result("Login", False, error=str(e))
        return False

def test_get_stock():
    print_header("Testing Get Stock Endpoint")
    try:
        response = requests.get(f"{API_URL}/zureo/stock/{TEST_SKU}")
        success = response.status_code == 200
        print_result("Get Stock", success, response.json() if success else None)
        return success
    except Exception as e:
        print_result("Get Stock", False, error=str(e))
        return False

def test_adjust_stock():
    print_header("Testing Adjust Stock Endpoint")
    try:
        response = requests.get(f"{API_URL}/zureo/ajustar/{TEST_SKU}/{TEST_QUANTITY}")
        success = response.status_code == 200
        print_result("Adjust Stock", success, response.json() if success else None)
        return success
    except Exception as e:
        print_result("Adjust Stock", False, error=str(e))
        return False

def run_all_tests():
    print_header("Starting API Tests")
    print(f"API URL: {API_URL}")
    print(f"Test SKU: {TEST_SKU}")
    print(f"Test Quantity: {TEST_QUANTITY}")
    
    results = {
        "Health Check": test_health_check(),
        "Login": test_login(),
        "Get Stock": test_get_stock(),
        "Adjust Stock": test_adjust_stock()
    }
    
    print_header("Test Results Summary")
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} | {test_name}")
        if not passed:
            all_passed = False
    
    print_header("Final Result")
    if all_passed:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 