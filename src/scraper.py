# load standard libraries
import re
import time
import json

# load testing library
from selenium import webdriver, common
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# load HTML and XML documents parser library
from bs4 import BeautifulSoup

'''
Utility Functions
'''
# function to return "<n/a>" value 
def try_or(fn):
    try:
        return fn()
    except:
        return "<n/a>"

# function to clean string
def cleaning_string(txt):
    txt = re.sub(r'<.*?>', '', txt)
    return txt

# function to get project url
def extract_project_url(df_input):
    list_url = []
    for ele in df_input["clickthrough_url"]:
        list_url.append("https://www.indiegogo.com" + ele)
    return list_url

# function to retry due to certain errors
def retry(fun, max_tries=10):
    for i in range(max_tries):
        try:
           time.sleep(0.3) 
           fun()
           break
        except Exception:
            continue
        
'''
Scrape data from Basic Section and Story Menu
'''
def scrape_basic_and_story(url):
    # chromedriver initialization
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    s = Service(r"chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)
    
    driver.implicitly_wait(10)
    driver.get(url)

    while True:
        try:
            driver.find_element(By.CLASS_NAME, "buttonSecondary buttonSecondary--gogenta buttonSecondary--medium").click()
            time.sleep(2)
        except common.exceptions.NoSuchElementException:
            break
    time.sleep(2)
    
    content = driver.page_source
    driver.quit()

    soup = BeautifulSoup(content, "lxml")
    
    tagline = try_or(lambda: soup.find("div", \
        class_="basicsSection-tagline").contents[0].strip())

    raised = try_or(lambda: soup.find("span", \
        class_="basicsGoalProgress-amountSold").contents[0].strip())

    backers = try_or(lambda: soup.find("span", \
        class_="basicsGoalProgress-claimedOrBackers").contents[0].strip())

    story = try_or(lambda: soup.find("div", \
        class_="routerContentStory-storyBody"))

    dict_res = {
        "tagline": tagline,
        "raised": raised,
        "backers" : backers,
        "story" : cleaning_string(str(story))
    }
    
    return dict_res

'''
Scrape data from FAQ menu
'''
def scrape_faq(url):
    # chromedriver initialization
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    s = Service(r"chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)
    
    driver.implicitly_wait(10)
    driver.get(url+"/#/faq")
    time.sleep(2)
    
    content = driver.page_source
    driver.quit()

    soup = BeautifulSoup(content, "lxml")
    
    list_of_faq = [e for e in soup.find_all("div", \
        class_="campaignFaq-container")]
    
    dict_res = {}
    if not list_of_faq:
        dict_res = "<n/a>"
    else:
        for idx, val in enumerate(list_of_faq):
            faq_qst = try_or(lambda: val.find("div", \
                class_="campaignFaq-question").contents[0].strip())

            faq_ans = try_or(lambda: val.find("div", \
                class_="campaignFaq-answer").contents[0].strip())

            dict_res[idx] = {
                "question": faq_qst,
                "answer": faq_ans
            }
    
    return dict_res

'''
Scrape data from Updates menu
'''
def scrape_updates(url):
    # chromedriver initialization
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    s = Service(r"chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)
    
    driver.implicitly_wait(10)
    driver.get(url+"/#/updates/all")

    while True:
        try:
            driver.find_element(by=By.LINK_TEXT, value="routerContentUpdate-readMore").click()
            time.sleep(2)
        except common.exceptions.NoSuchElementException:
            break
    time.sleep(2)
    
    content = driver.page_source
    driver.quit()

    soup = BeautifulSoup(content, "lxml")
    
    list_of_upd = [e for e in soup.find_all("div", \
        class_="routerContentUpdate")]
    
    dict_res = {}
    if not list_of_upd:
        dict_res = "<n/a>"
    else:
        for idx, val in enumerate(list_of_upd):
            name = try_or(lambda: val.find("div", \
                class_="routerContentUpdate-name").contents[0].strip())

            datetime = try_or(lambda: val.find("div", \
                class_="routerContentUpdate-date").contents[0].strip())

            update = try_or(lambda: val.find("div", \
                class_="sharedStyle-campaignUpdateUgc"))

            dict_res[idx] = {
                "name": name,
                "datetime": datetime,
                "update": cleaning_string(str(update))
            }
    
    return dict_res

'''
Scrape data from Discussion menu
'''
def scrape_discussion(url):
    # chromedriver initialization
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    s = Service(r"chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)
    
    driver.implicitly_wait(10)
    driver.get(url+"/#/discussion")\

    while True:
        try:
            element = driver.find_element(by=By.LINK_TEXT, value="Show more comments")
            element.click()
            time.sleep(2)
        except common.exceptions.NoSuchElementException:
            break

    while True:
        try:
            element = driver.find_element(by=By.LINK_TEXT, value="Show 1 more reply")
            element.click()
            time.sleep(2)
        except common.exceptions.NoSuchElementException:
            break
    time.sleep(2)
    
    content = driver.page_source
    driver.quit()

    soup = BeautifulSoup(content, "lxml")
    
    list_of_dsc = [e for e in soup.find_all("li", \
        class_="discussionThread-parentComment")]
    
    dict_res = {}
    if not list_of_dsc:
        dict_res = "<n/a>"
    else:
        for idx, val in enumerate(list_of_dsc):
            dsc_author = try_or(lambda: val.find("a", \
                class_="discussionSingleComment-authorName").contents[0].strip())

            dsc_text = try_or(lambda: val.find("div", \
                class_="discussionSingleComment-bodyMarkup"))
            
            dsc_datetime = try_or(lambda: val.find("span", \
                class_="discussionSingleComment-timestamp")["title"])

            dsc_vote_up = try_or(lambda: val.find("span", \
                class_="buttonsVote-countUp").contents[0].strip())
                    
            dsc_vote_down = try_or(lambda: val.find("span", \
                class_="buttonsVote-countDown").contents[0].strip())

            list_of_cmt = [e for e in val.find_all("div", \
                class_="discussionSingleComment")]
            dict_cmts = {}
            if not list_of_cmt:
                dict_cmts = "<n/a>"
            else:
                for idx2, val2 in enumerate(list_of_cmt):
                    cmt_author = try_or(lambda: val2.find("a", \
                        class_="discussionSingleComment-authorName").contents[0].strip())
                    
                    cmt_text = try_or(lambda: val2.find("div", \
                        class_="discussionSingleComment-bodyMarkup"))
                    
                    cmt_datetime = try_or(lambda: val2.find("span", \
                        class_="discussionSingleComment-timestamp")["title"])
                    
                    cmt_vote_up = try_or(lambda: val2.find("span", \
                        class_="buttonsVote-countUp").contents[0].strip())
                    
                    cmt_vote_down = try_or(lambda: val2.find("span", \
                        class_="buttonsVote-countDown").contents[0].strip())
                    
                    if cmt_author != "<n/a>":
                        dict_cmts[idx2] = {
                            "cmt_author": cmt_author,
                            "cmt_text": cleaning_string(str(cmt_text)),
                            "cmt_datetime": cmt_datetime,
                            "cmt_vote_up": cmt_vote_up,
                            "cmt_vote_down": cmt_vote_down
                        }

                if dsc_author != "<n/a>":
                    dict_res[idx] = {
                        "dsc_name": dsc_author,
                        "dsc_text": cleaning_string(str(dsc_text)),
                        "dsc_datetime": dsc_datetime,
                        "dsc_vote_up": dsc_vote_up,
                        "dsc_vote_down": dsc_vote_down,
                        "dsc_comments": dict_cmts                
                    }
    
    return dict_res

'''
Scrape data from Comments menu
'''
def scrape_comments(url):
    # chromedriver initialization
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    s = Service(r"chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)
    
    driver.implicitly_wait(10)
    driver.get(url+"/#/comments")
    
    while True:
        try:
            element = driver.find_element(by=By.LINK_TEXT, value="See More Comments")
            element.click()
            time.sleep(2)
        except common.exceptions.NoSuchElementException:
            break

    while True:
        try:
            element = driver.find_element(by=By.LINK_TEXT, value="more reply")
            element.click()
            time.sleep(2)
        except common.exceptions.NoSuchElementException:
            break
    
    while True:
        try:
            element = driver.find_element(by=By.LINK_TEXT, value="more replies")
            element.click()
            time.sleep(2)
        except common.exceptions.NoSuchElementException:
            break
    time.sleep(2)
    
    content = driver.page_source
    driver.quit()

    soup = BeautifulSoup(content, "lxml")
    
    list_of_cmts = [e for e in soup.find_all("div", \
        class_="routerContentComment")]
    
    dict_res = {}
    if not list_of_cmts:
        dict_res = "<n/a>"
    else:
        for idx, val in enumerate(list_of_cmts):
            cmt_author = try_or(lambda: val.find("a", \
                class_="routerContentComment-authorName").contents[0].strip())

            cmt_monthstamp = try_or(lambda: val.find("span", \
                class_="routerContentComment-subheader").contents[0].strip())
            
            cmt_text = try_or(lambda: val.find("div", \
                class_="routerContentComment-body"))

            cmt_vote_up = try_or(lambda: val.find("span", \
                class_="buttonsVote-countUp").contents[0].strip())
                    
            cmt_vote_down = try_or(lambda: val.find("span", \
                class_="buttonsVote-countDown").contents[0].strip())
            
            list_of_rpl = [e for e in val.find_all("div", \
                class_="is-gapless-singleline")]
            dict_rpls = {}
            if not list_of_rpl:
                dict_rpls = "<n/a>"
            else:
                for idx2, val2 in enumerate(list_of_rpl):
                    rpl_author = try_or(lambda: val2.find("a", \
                        class_="routerContentComment-replyAuthorName").contents[0].strip())
                    
                    rpl_text = try_or(lambda: val2.find("div", \
                        class_="routerContentComment-replyBody"))
                    
                    rpl_monthstamp = try_or(lambda: val2.find("span", \
                        class_="routerContentComment-replyTimestamp").contents[0].strip())
                    
                    if rpl_author != "<n/a>":
                        dict_rpls[idx2] = {
                            "rpl_author": rpl_author,
                            "rpl_text": cleaning_string(str(rpl_text)),
                            "rpl_monthstamp": rpl_monthstamp
                        }

                if cmt_author != "<n/a>":
                    dict_res[idx] = {
                        "cmt_author": cmt_author,
                        "cmt_monthstamp": cmt_monthstamp,
                        "cmt_text": cleaning_string(str(cmt_text)),
                        "cmt_vote_up": cmt_vote_up,
                        "cmt_vote_down": cmt_vote_down,
                        "cmt_reply": dict_rpls                
                    }
    
    return dict_res

'''
Merge all menu scraper
'''
def scrapes(url):
    dict_out = {
        "site": url,
        "basic_story": scrape_basic_and_story(url),
        "faq": scrape_faq(url),
        "updates": scrape_updates(url),
        "disscusion": scrape_discussion(url),
        "comments": scrape_comments(url)
    }
    return dict_out