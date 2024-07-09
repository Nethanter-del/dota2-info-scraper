from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://ru.dotabuff.com/'
target = input('Target(nickname): ')
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=options)
print('request to dotabuff.com')
driver.get(url)
print('Completed')
print('Search')
def checker(target):
    driver.execute_script(f"document.getElementById('q').value = '{target}';")
    driver.execute_script("document.forms[0].submit();")
    wait = WebDriverWait(driver, 3)
    profile_link = driver.current_url
    parts = profile_link.split("/")
    buff_id = parts[-1]
    metric_link = profile_link + "/scenarios?metric=all"
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='header-content-secondary']")))
        print("Getting statistics")
    except Exception:
        print("Timeout")
    driver.get(metric_link)
    div_element = driver.find_element(By.CLASS_NAME, "header-content-secondary")
    time_element = div_element.find_element(By.TAG_NAME, "time")
    last_game = time_element.get_attribute("title")
    rank_element = div_element.find_element(By.CLASS_NAME, "rank-tier-wrapper")
    rank_info = rank_element.get_attribute("oldtitle")
    if ":" in rank_info:
        rank = rank_info.split(":")[1].strip()
    else:
        rank = "Unknown"
    table_rows = driver.find_elements(By.TAG_NAME, "tr")
    all_matches = ' - '
    win_rate = ' - '
    played_time = ' - '
    for row in table_rows:
        if "All matches" in row.text:
            columns = row.find_elements(By.TAG_NAME, "td")
            all_matches = columns[1].text 
            win_rate = columns[2].text
            played_time = columns[3].text
            break 
    print()
    print("Profile:", target)
    print("DotaBuff id:", buff_id)
    print("Last game:", last_game)
    print("Possible rank:", rank)
    print("All matches:", all_matches)
    print("Win rate:", win_rate)
    print("Playtime:", played_time)
try:
    checker(target)
except Exception:
    print('User not found')
driver.quit()