from selenium import webdriver
import pandas as pd
import time

url = 'https://www.amazon.com/s?rh=n%3A16225007011&fs=true' # Delete reference on the url 'ref...'

driver = webdriver.Chrome("chromedriver.exe") 
chrome_options = webdriver.ChromeOptions()

column_names = ['name', 'rating','rating_count','price']
df = pd.DataFrame(columns = column_names)


#_______________________________________________________
i=0
while i<20:
    i+=1
    url = 'https://www.amazon.com/s?i=computers-intl-ship&rh=n%3A16225007011&fs=true&page=' + str(i)
    driver.get(url) 
    products = driver.find_elements_by_class_name('sg-col-4-of-12')
    for product in products:
        try:                                      
            name = product.find_element_by_class_name('a-size-base-plus').text
        except:
            continue
        # get the rating________________________________________________________________________________
        try:
            stars = product.find_element_by_class_name('a-popover-trigger')
            stars.click()
            time.sleep(1.5)  
            rating_list = stars.find_elements_by_xpath("//span[@data-hook='acr-average-stars-rating-text']")
            rating = None
            for rate in rating_list:
                rating = str(rating) + rate.text
            rating = rating.replace(' out of 5','').replace('None','') 
        except:
            pass
        # ______________________________________________________________________________________________
        try:
            rating_count = product.find_element_by_class_name('a-size-base').text
        except:
            pass
        try:
            whole_price = product.find_element_by_class_name('a-price-whole').text
            fraction_price = product.find_element_by_class_name('a-price-fraction').text
            price = whole_price + '.' + fraction_price
        except:
            price = None
        df.loc[len(df)] = [name, rating, rating_count,price]
        print(df.tail(1))
 

    df.to_csv('details.csv', sep="\t",index=False)
