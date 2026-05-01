from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# ================= CONFIG =================
BASE_URL = "http://127.0.0.1:8000"

USERS = [
    {"username": "D-1005", "password": "mededu40", "role": "non-student"},
    {"username": "L-1003", "password": "mededu40", "role": "non-student"},
    {"username": "I-1006", "password": "mededu40", "role": "non-student"},
    {"username": "F-1008", "password": "mededu40", "role": "non-student"},
    {"username": "W-1007", "password": "mededu40", "role": "non-student"},
    {"username": "A-1009", "password": "mededu40", "role": "non-student"},
    {"username": "DS-1004", "password": "mededu40", "role": "student"},
    {"username": "MS-1002", "password": "mededu40", "role": "student"},
]

# ================= DRIVER =================
driver = webdriver.Edge()
wait = WebDriverWait(driver, 10)


# ================= LOGIN =================
def login(user_id, password):
    driver.get(f"{BASE_URL}/login/")

    wait.until(EC.presence_of_element_located((By.NAME, "mededu_id"))).send_keys(user_id)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

    try:
        wait.until(EC.url_contains("dashboard"))
        print(f"✅ Login success: {user_id}")
    except TimeoutException:
        print(f"❌ Login failed: {user_id}")


# ================= LOGOUT =================
def logout():
    try:
        driver.get(f"{BASE_URL}/logout/")
        wait.until(EC.url_contains("login"))
        print("✅ Logout success")
    except:
        print("❌ Logout failed")


# ================= NAVBAR CHECK =================
def check_navbar(role):
    print("🔍 Checking navbar...")

    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "nav")))

        course = driver.find_elements(By.LINK_TEXT, "Course & Syllabus")
        exam = driver.find_elements(By.LINK_TEXT, "Exam")
        result = driver.find_elements(By.LINK_TEXT, "Result")

        if role == "student":
            if course and exam and result:
                print("✅ Student navbar OK")
            else:
                print("❌ Student navbar missing items")
        else:
            if not course and not exam and not result:
                print("✅ Non-student navbar OK")
            else:
                print("❌ Non-student navbar error")

    except:
        print("❌ Navbar check failed")


# ================= SUBJECT PAGE =================
def test_subject_access(role):
    print("🔍 Testing subject page...")

    driver.get(f"{BASE_URL}/subject/anatomy/")

    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        page = driver.page_source

        if role == "student":
            if "Syllabus" in page:
                print("✅ Subject access OK")
            else:
                print("❌ Subject page broken")
        else:
            if "dashboard" in driver.current_url:
                print("✅ Non-student blocked correctly")
            else:
                print("❌ Unauthorized access")

    except:
        print("❌ Subject test failed")


# ================= PDF LOAD =================
def test_pdf(role):
    if role != "student":
        return

    print("🔍 Testing PDF load...")

    driver.get(f"{BASE_URL}/subject/anatomy/")

    try:
        iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        if iframe:
            print("✅ PDF loaded")
    except:
        print("❌ PDF not loaded")


# ================= EXAM NOTICE =================
def test_exam_notice(role):
    if role != "student":
        return

    print("🔍 Testing exam notice...")

    driver.get(f"{BASE_URL}/exam/card/1/")

    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("✅ Exam notice page loaded")
    except:
        print("❌ Exam notice failed")


# ================= RESULT =================
def test_result():
    print("🔍 Testing result page...")

    driver.get(f"{BASE_URL}/result/")

    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        print("✅ Result loaded")
    except:
        print("❌ Result failed")


# ================= PAYMENT =================
def test_payment(role):
    print("🔍 Testing payment...")

    driver.get(f"{BASE_URL}/payment/")

    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        if role == "student":
            form = driver.find_elements(By.TAG_NAME, "form")
            if form:
                print("✅ Payment form OK")
            else:
                print("❌ Payment form missing")
        else:
            print("✅ Non-student payment view OK")

    except:
        print("❌ Payment test failed")


# ================= MAIN TEST =================
for user in USERS:
    print("\n==============================")
    print(f"🔹 Testing user: {user['id']}")

    login(user["id"], user["password"])

    check_navbar(user["role"])
    test_subject_access(user["role"])
    test_pdf(user["role"])
    test_exam_notice(user["role"])
    test_result()
    test_payment(user["role"])

    logout()

driver.quit()

print("\n🎉 ALL TESTS COMPLETED")