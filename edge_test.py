from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ===== DRIVER =====
driver = webdriver.Edge()
wait = WebDriverWait(driver, 10)

# ===== USERS (ID + PASSWORD) =====
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

# ===== LOOP TEST =====
for uid, password in users:
    print(f"\n🔹 Testing user: {uid}")

    driver.get("http://127.0.0.1:8000/login/")

    # wait until input visible
    wait.until(EC.visibility_of_element_located((By.NAME, "mededu_id")))

    # ===== INPUT =====
    id_box = driver.find_element(By.NAME, "mededu_id")
    pass_box = driver.find_element(By.NAME, "password")

    id_box.clear()
    id_box.send_keys(uid)

    pass_box.clear()
    pass_box.send_keys(password)

    # ===== LOGIN =====
    driver.find_element(By.CLASS_NAME, "auth-btn").click()

    time.sleep(4)

    # ===== CHECK SUCCESS =====
    current_url = driver.current_url

    if "login" not in current_url:
        print(f"✅ Login SUCCESS → {uid}")
    else:
        print(f"❌ Login FAILED → {uid}")

    # ===== LOGOUT =====
    try:
        logout = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
        )
        logout.click()
        time.sleep(2)
    except:
        print("⚠️ Logout not found")

# শেষ
time.sleep(3)
driver.quit()