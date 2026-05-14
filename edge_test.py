from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options

import time


# ================= USERS =================

USERS = [

    {"username": "D-1006", "password": "mededu40", "role": "doctor"},

    {"username": "L-1008", "password": "mededu40", "role": "library staff"},

    {"username": "I-1005", "password": "mededu40", "role": "intern doctor"},

    {"username": "F-1004", "password": "mededu40", "role": "faculty"},

    {"username": "W-1007", "password": "mededu40", "role": "ward authority"},

    {"username": "A-1009", "password": "mededu40", "role": "admin"},

    {"username": "DS-1003", "password": "mededu40", "role": "student"},

    {"username": "MS-1002", "password": "mededu40", "role": "student"},

]


# ================= DRIVER SETUP =================

BASE_URL = "http://127.0.0.1:8000/"

options = Options()

options.add_argument("--disable-gpu")

service = Service("msedgedriver.exe")

driver = webdriver.Edge(
    service=service,
    options=options
)

driver.maximize_window()

driver.implicitly_wait(10)

wait = WebDriverWait(driver, 15)


# ================= LOGIN FUNCTION =================

def login(user):

    driver.get(BASE_URL)

    print("\n=================================")
    print(f"Testing Role: {user['role']}")
    print("=================================")

    username = wait.until(
        EC.presence_of_element_located(
            (By.NAME, "mededu_id")
        )
    )

    password = wait.until(
        EC.presence_of_element_located(
            (By.NAME, "password")
        )
    )

    username.clear()
    password.clear()

    username.send_keys(user["username"])
    password.send_keys(user["password"])

    login_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit']")
        )
    )

    login_btn.click()

    time.sleep(2)

    print("Login Successful")


# ================= OPEN PAGE =================

def open_page(link_text):

    try:

        page = wait.until(
            EC.element_to_be_clickable(
                (By.PARTIAL_LINK_TEXT, link_text)
            )
        )

        page.click()

        print(f"{link_text} Page Opened")

        time.sleep(1)

    except Exception:

        print(f"{link_text} Not Available")


# ================= NAVIGATION TEST =================

def test_navigation():

    print("Testing Navbar...")

    links = driver.find_elements(By.TAG_NAME, "a")

    print(f"Navbar Links Found: {len(links)}")

    pages = [

        "Profile",
        "Notification",
        "Library",
        "Payment",
        "Result",
        "Exam",
        "Status",
        "Logout"

    ]

    for page in pages:

        open_page(page)


# ================= LOGOUT =================

def logout():

    try:

        logout_btn = wait.until(
            EC.element_to_be_clickable(
                (By.PARTIAL_LINK_TEXT, "Logout")
            )
        )

        logout_btn.click()

        time.sleep(2)

        print("Logout Success")

    except Exception:

        print("Logout Failed")


# ================= MAIN TEST LOOP =================

for user in USERS:

    try:

        login(user)

        test_navigation()

        logout()

        print(f"TEST PASSED for {user['role']}")

    except Exception as e:

        print(f"TEST FAILED for {user['role']}")
        print("Message:", e)

    finally:

        driver.get(BASE_URL)


# ================= END =================

print("\nALL TESTING COMPLETED")

driver.quit()