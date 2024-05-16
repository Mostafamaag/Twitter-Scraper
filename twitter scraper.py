import datetime
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time



#this function not used for now 
#takes the date as string and proccess it (remove unwanted chars)
#return it as datetime object
def datetime_preprcessor(datetime_str):
    datetime_str = datetime_str.replace('T',' ').replace('Z','0')
    format = "%Y-%m-%d %H:%M:%S.%f"
    datetime_object = datetime.strptime(datetime_str,format)
    return datetime_object

def twitter_scrapper(url):

    #path = 'C:\webdrivers\chromedriver.exe'
    #service = webdriver.ChromeService(executable_path=path)
    #driver = webdriver.Chrome(service)


    driver = webdriver.Chrome() #create browser instance
    driver.get(url) #open url in virtual brower
    time.sleep(5) #wait 5 seconds


    # scroll down function
    def scroller():

        height = driver.execute_script("return document.body.scrollHeight") # get scroll height
        
        while True:
            #driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")

            if height == new_height: # break if we reach to the end of the page
                break

            height = new_height
        
    scroller()    


    tweets = driver.find_elements(By.XPATH, '//div[@data-testid]//article[@data-testid="tweet"]')
    TweetsTime = []

    # get tweets, time and store them in list
    for tweet in tweets:
        text = tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
        date = tweet.find_element(By.XPATH, './/time').get_attribute("datetime")
        TweetsTime.append((text,date))
        #print(text)

    driver.close()

    numbers = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
    WordFreq = {}

    #data preprocessing
    #count all words that start with $ 
    for tweet,t in TweetsTime:

        tweet_words = tweet.split()
        for word in tweet_words:
            if word.startswith('$') and not word[1] in numbers: #check word is vaild
                if word in WordFreq:
                    WordFreq[word] += 1
                else:
                    WordFreq[word] = 1

    return WordFreq


def run_scrapper(accounts, minutes):

    time_in_secondes = int(minutes) * 60

    while True:

        for acc in twitter_accounts:
            word_freq = twitter_scrapper(acc)
        
            #print needed data
            print("url :", acc)
            for word, freq in word_freq.items():
                print(word,"was mentioned",freq, "times in the last",minutes, "minutes")
            
            print("-------------------------------------------------------------")
        
        print("####################################################################")
        time.sleep(time_in_secondes) # wait x minutes to scrape again


if __name__ == "__main__":
    
    twitter_accounts = [
        "https://twitter.com/Mr_Derivatives",
        "https://twitter.com/warrior_0719",
        "https://twitter.com/ChartingProdigy",
        "https://twitter.com/allstarcharts",
        "https://twitter.com/yuriymatso",
        "https://twitter.com/TriggerTrades",
        "https://twitter.com/AdamMancini4",
        "https://twitter.com/CordovaTrades",
        "https://twitter.com/Barchart",
        "https://twitter.com/RoyLMattox",
    ]
    time_in_minutes = input("Enter the time in minutes : ")
    run_scrapper(twitter_accounts, time_in_minutes)


