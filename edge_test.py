from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ===== DRIVER =====
driver = webdriver.Edge()
driver.maximize_window()

wait = WebDriverWait(driver, 15)

# ===== USERS =====
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

# ===== LOOP =====
for uid, password in users:

    print(f"\n🔹 Testing user: {uid}")

    # ===== OPEN LOGIN =====
    driver.get("http://127.0.0.1:8000/login/")

    wait.until(EC.visibility_of_element_located((By.NAME, "mededu_id")))

    # ===== INPUT =====
    driver.find_element(By.NAME, "mededu_id").clear()
    driver.find_element(By.NAME, "mededu_id").send_keys(uid)

    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "password").send_keys(password)

    driver.find_element(By.CLASS_NAME, "auth-btn").click()

    # ===== WAIT LOGIN SUCCESS =====
    try:
        wait.until(EC.url_changes("http://127.0.0.1:8000/login/"))
        print(f"✅ Login SUCCESS → {uid}")
        time.sleep(2)

    except:
        print(f"❌ Login FAILED → {uid}")
        continue

    # ===== PROFILE TEST =====
    try:
        profile = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Profile"))
        )
        profile.click()

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "auth-card")))
        print("✅ Profile opened")

        time.sleep(2)

    except Exception as e:
        print("❌ Profile issue")
        print("DEBUG:", e)

    # ===== 🔥 LOGOUT FIX (BEST METHOD) =====
    try:
        # 👉 direct logout URL (100% reliable)
        driver.get("http://127.0.0.1:8000/logout/")

        # wait login page
        wait.until(EC.visibility_of_element_located((By.NAME, "mededu_id")))

        print("✅ Logout SUCCESS")

        time.sleep(2)

    except Exception as e:
        print("❌ Logout issue")
        print("DEBUG:", e)

# ===== END =====
driver.quit()