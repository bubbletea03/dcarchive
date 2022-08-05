from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager
import os

def save_pageArchive(url):
    MAX_WAIT = 5

    driver = get_driver()
    driver.get(url)
    driver.implicitly_wait(MAX_WAIT)

    soup = bs(driver.page_source, 'lxml')
    posts = soup.find_all("tr", class_="us-post")

    already_filelist = os.listdir(os.getcwd()+"/posts")

    for post in posts:
        data = {
            "num": post.find("td", class_="gall_num").text,
            "title": post.find("a").text,
        }

        if data["num"] in already_filelist: # 이미 저장해논거면 넘김
            continue

        if post["data-type"] == "icon_notice": #공지글 넘김
            continue
    
        try:
            driver.get("https://gall.dcinside.com" + post.find("a")["href"])
            driver.implicitly_wait(MAX_WAIT)
        except:
            continue

        content_div = bs(driver.page_source, 'lxml').find("div", class_="write_div")
        data["content"] = content_div.text if content_div else ""

        remove_ad_banner(driver)
        try:
            with open(os.getcwd()+"/posts/"+data["num"], "w", encoding="utf8") as f:
                f.write(data["title"])
                f.write(data["content"])
            driver.execute_script("window.scrollTo(135, 230)")
            driver.execute_script("document.body.style.zoom='80%'")
            driver.get_screenshot_as_file(os.getcwd()+"/screenshots/"+data["num"]+".png")
        except:
            continue

def remove_ad_banner(driver):
    try:
        banner_closeBtn = driver.find_element(By.ID, "wif_adx_banner_close")
        banner_closeBtn.click()
        time.sleep(0.5) # 내려가는 시간이 있으므로 잠깐 정지
    except:
        pass # 배너 존재하지 않음
    
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument("window-size=640x640")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")

    return driver