from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# ================= CONFIG =================
BASE_URL = "http://127.0.0.1:8000"

# ===== USERS (FIXED) =====
USERS = [
    {"username": "DR-6287", "password": "NiLa40", "role": "non-student"},
    {"username": "LB-5543", "password": "ShIhAb40", "role": "non-student"},
    {"username": "I-1006", "password": "PrInCe40", "role": "non-student"},
    {"username": "F-1008", "password": "TaMaNnA40", "role": "non-student"},
    {"username": "WA-2384", "password": "LiThI40", "role": "non-student"},
    {"username": "A-1010", "password": "MaHa40", "role": "non-student"},
    {"username": "DS-1012", "password": "AzMiNe40", "role": "student"},
    {"username": "MS-1013", "password": "JaFrIn40", "role": "student"},
]

# ================= DRIVER =================
driver = webdriver.Edge()


def login(username, password):
    driver.get(f"{BASE_URL}/login/")
    time.sleep(1)

    driver.find_element(By.NAME, "mededu_id").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

    time.sleep(2)


def logout():
    try:
        driver.get(f"{BASE_URL}/logout/")
        time.sleep(2)
        print("✅ Logout success")
    except:
        print("❌ Logout failed")


def check_student_features(role):
    print("🔍 Checking UI visibility...")

    course = driver.find_elements(By.LINK_TEXT, "Course & Syllabus")
    exam = driver.find_elements(By.LINK_TEXT, "Exam")
    result = driver.find_elements(By.LINK_TEXT, "Result")

    if role == "student":
        if course and exam and result:
            print("✅ Student UI visible")
        else:
            print("❌ Student UI missing")
    else:
        if not course and not exam and not result:
            print("✅ Non-student UI hidden")
        else:
            print("❌ Non-student UI visible (ERROR)")


def test_subject_access(role):
    print("🔍 Testing subject access...")

    driver.get(f"{BASE_URL}/subject/anatomy/")
    time.sleep(2)

    if role == "student":
        if "Syllabus" in driver.page_source:
            print("✅ Student can access subject")
        else:
            print("❌ Student cannot access subject")
    else:
        if "Access Denied" in driver.page_source:
            print("✅ Non-student blocked")
        else:
            print("❌ Non-student accessed subject (ERROR)")


def test_pdf_loading(role):
    if role != "student":
        return

    print("🔍 Testing PDF loading...")

    driver.get(f"{BASE_URL}/subject/anatomy/")
    time.sleep(2)

    iframe = driver.find_elements(By.TAG_NAME, "iframe")

    if iframe:
        print("✅ PDF loaded")
    else:
        print("❌ PDF not loaded")


# ================= MAIN TEST =================

for user in USERS:
    print("\n==============================")
    print(f"🔹 Testing user: {user['username']}")

    login(user["username"], user["password"])

    # UI test
    check_student_features(user["role"])

    # subject access
    test_subject_access(user["role"])

    # pdf test
    test_pdf_loading(user["role"])

    # logout
    logout()

driver.quit()

print("\n🎉 ALL TESTS COMPLETED")