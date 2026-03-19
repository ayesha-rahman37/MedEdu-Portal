from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Edge()
driver.maximize_window()

wait = WebDriverWait(driver, 15)

users = [
    ("DR-6287", "NiLa40"),
    ("LB-5543", "ShIhAb40"),
    ("I-1006", "PrInCe40"),
    ("F-1008", "TaMaNnA40"),
    ("WA-2384", "LiThI40"),
    ("A-1010", "MaHa40"),
    ("DS-1012", "AzMiNe40"),
    ("MS-1013", "JaFrIn40"),
]

for uid, password in users:

    print(f"\n🔹 Testing user: {uid}")

    # ===== LOGIN PAGE =====
    driver.get("http://127.0.0.1:8000/login/")

    wait.until(EC.visibility_of_element_located((By.NAME, "mededu_id")))

    driver.find_element(By.NAME, "mededu_id").clear()
    driver.find_element(By.NAME, "mededu_id").send_keys(uid)

    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "password").send_keys(password)

    driver.find_element(By.CLASS_NAME, "auth-btn").click()

    # ===== FIX: WAIT URL CHANGE =====
    try:
        wait.until(EC.url_changes("http://127.0.0.1:8000/login/"))
        print(f"✅ Login SUCCESS → {uid}")
        time.sleep(2)

    except:
        print(f"❌ Login FAILED → {uid}")
        continue

    # ===== PROFILE =====
    try:
        profile = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Profile"))
        )
        profile.click()

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "auth-card")))
        print("✅ Profile opened")

        time.sleep(2)

    except:
        print("❌ Profile issue")

    # ===== 🔥 LOGOUT (ULTRA FIX) =====
    try:
        # navbar ensure visible
        driver.execute_script("window.scrollTo(0, 0);")

        logout = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
        )

        # JS click (important)
        driver.execute_script("arguments[0].click();", logout)

        # wait login page
        wait.until(EC.visibility_of_element_located((By.NAME, "mededu_id")))

        print("✅ Logout SUCCESS")
        time.sleep(2)

    except Exception as e:
        print("❌ Logout issue")
        print("DEBUG:", e)

driver.quit()