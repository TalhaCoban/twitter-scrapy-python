
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv


username = ""
password = ""

hashtag = "kaan"



def get_all_tweets(username, password, hashtag):
    
    driver = webdriver.Firefox()
    driver.get("https://twitter.com")
    time.sleep(3)


    login_button_xpath = "/html/body/div/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a"
    login_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, login_button_xpath))
    )
    login_input.click()


    username_xpath = "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input"
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, username_xpath))
    )
    username_input.send_keys(username)


    forward_xpath = "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div"
    forward_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, forward_xpath))
    )
    forward_button.click()

    password_xpath = "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input"
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, password_xpath))
    )
    password_input.send_keys(password)

    login_button_xpath = "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div"
    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, login_button_xpath))
    )
    login_button.click()
    time.sleep(2)

    driver.get("https://twitter.com/explore")

    explore_input = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[1]/div[2]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input"
    explore = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, explore_input))
    )
    explore.clear()
    explore.send_keys(hashtag, Keys.ENTER)
    """
    latest_xpath = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a"
    latest = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, latest_xpath))
    )
    latest.click()
    """
    time.sleep(3)


    all_tweets = list()
    twts = list()

    last_position = driver.execute_script("return window.pageYOffset;")
    scrolling = True

    while scrolling:
        try:
            time.sleep(3)
            tweets_xpath = '//div[@data-testid="tweetText"]'
            tweets = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, tweets_xpath))
            )

            users_xpath = '//div[@data-testid="User-Name"]'
            users = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, users_xpath))
            )

            group_xpath = '//div[@role="group"]'
            group = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, group_xpath))
            )

            times = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "time"))
            )

            for user, tweet, el, tme in zip(users, tweets, group, times):
                
                if tweet.get_attribute("lang") == "en":
                    continue
                
                name = user.text.split("@")[0].strip()
                username = "@" + user.text.split("@")[1].split()[0]
                tweet = tweet.text
                comment, retweet, like, watching = 0, 0, 0, 0
                for e in el.get_attribute("aria-label").split(","):
                    if e.strip().endswith("yanıt"):
                        comment = int(e.split()[0].strip())
                    elif e.strip().endswith("Retweet"):
                        retweet = int(e.split()[0].strip())
                    elif e.strip().endswith("beğeni"):
                        like = int(e.split()[0].strip())
                    elif e.strip().endswith("görüntülenme"):
                        watching = int(e.split()[0].strip())
                    else:
                        pass
                tme = tme.get_attribute("datetime")
                
                data = (
                        name,
                        username,
                        tweet,
                        comment,
                        retweet,
                        like,
                        watching,
                        tme
                    )
                if (data not in all_tweets) and (tweet not in twts):
                    twts.append(tweet)
                    all_tweets.append(data)
                
        except:
            pass
                
        def smooth_scroll_to_bottom(driver, current_scroll, scroll_speed):
            scroll_height = driver.execute_script("return document.documentElement.scrollHeight")
            if current_scroll < scroll_height:
                driver.execute_script("window.scrollTo(0, arguments[0]);", current_scroll)
                current_scroll += scroll_speed 

            return current_scroll
        
        curr_position = smooth_scroll_to_bottom(driver, last_position, 1000)
        
        if last_position == curr_position:
            scrolling = False
        
        last_position = curr_position
        print(len(all_tweets))


    #driver.close()
        
        
    with open('tweets.csv', 'w', newline='', encoding='utf-8') as file:
        header = ['isim', 'Kullanıcı ismi', 'tweet', 'yorum', 'retweet', 'beğeni', 'görüntülenme', 'tarih']
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(all_tweets)
    

    
if __name__ == "__main__":
    get_all_tweets(username, password, hashtag)
    