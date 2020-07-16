from __future__ import division
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import collections
from sendMail import sendM
from receiveMail import receiveM
#Take out privateInfo and input your own private information
import privateInfo
import json

class itemTracker:
    items = []
    inStock = []
    notInStock = {}
    
    def __init__(self,username,password,items):
        self.username = username
        self.password = password
        self.items = items
        chrome_options = Options()
        #Change information to your respective file destinations
        chrome_options.add_argument("--user-data-dir=C:\\Users\\Shreyas\\AppData\\Local\\Google\\Chrome\\User")
        chrome_options.add_argument('--profile-directory=Profile 1')
        self.driver = webdriver.Chrome(r'C:\Users\Shreyas\Downloads\chromedriver_win32\chromedriver.exe')

    def logIn(self):
        self.driver.get('https://www.amazon.com/')
        if len(self.items) ==0:
            self.driver.close()
            raise Exception("No items to check")
        try:
            element = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, "/html/body"))
            )
        except:
            raise Exception("Amazon is not reachable at the moment - Log In ")
            self.driver.quit()
        self.driver.find_element_by_xpath('//*[@id="nav-link-accountList"]/div/span').click()
        try:
            element = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, "/html/body"))
            )
        except:
            raise Exception("Amazon is not reachable at the moment - Username ")
            self.driver.quit()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/form/div/div/div/div[1]/input[1]").send_keys(self.username)
        self.driver.find_element_by_xpath('//*[@id="continue"]').click()
        try:
            element = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, "/html/body"))
            )
        except:
            raise Exception("Amazon is not reachable at the moment - Password ")
            self.driver.quit()
        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div/form/div/div[1]/input").send_keys(self.password)
        self.driver.find_element_by_xpath('//*[@id="signInSubmit"]').click()
        sleep(15)
    def itemAvailability(self):
        if len(self.items) ==0:
            self.driver.close()
            raise Exception("No items to check")
        for item in self.items:
            self.driver.get(item)
            try:
                element = WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_element_located((By.XPATH, "/html/body"))
                )
            except:
                raise Exception("Amazon is not reachable at the moment - Items")
                self.driver.quit()
            stock = self.driver.find_element_by_xpath(
                '// *[ @ id = "availability"] / span').text
            if stock == 'In Stock.':
                self.inStock.append(item)
            else:
                self.notInStock[item] = stock
    def addToCart(self):
        with open('list.txt', "r") as file:
            filedata = file.read()
        for item in self.inStock:
            self.driver.get(item)
            try:
                element = WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_element_located((By.XPATH, "/html/body"))
                )
            except:
                raise Exception("Amazon is not reachable at the moment - Add to Cart")
                self.driver.quit()
            try:
                self.driver.find_element_by_xpath('//*[@id="add-to-cart-button"]').click()
            except:
                print("Unable to add "+self.driver.find_element_by_xpath('//*[@id="productTitle"]').text)
            if item in self.items:
                self.items.remove(item)
            filedata = filedata.replace(item, "")
            with open('list.txt', "w") as file:
                file.write(filedata)



file = open('list.txt','w+')
items = file.readlines()
print(items)
tempItems =[]
for item in items:
    tempItems.append(item)
x = True

while x:
    item = input("Enter your Item to the List and type 'done' when done: ")
    if item[0] =='h' or item =='done':
        items.append("%s"%item)
        if item =='done':
            items.remove('done')
            x = False
    else:
        continue

compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

if compare(tempItems,items)==False:
    file = open('list.txt','w')
    for i in range(len(items)):
        file.write(items[i])
        file.write("\n")
file.close()

items[:] = [x for x in items if x != "\n"]
print(items)
#Input username and password
tracker = itemTracker(privateInfo.amazonUsername,privateInfo.amazonPassword,items)
#Unable to log in due to Amazon bot protection
#tracker.logIn()
tracker.itemAvailability()
tracker.addToCart()


tracker.driver.close()
receive_mail = receiveM()
mail_string = receive_mail.receive()
print(mail_string)

send = sendM("These items were in Stock: "+str(tracker.inStock)+" while these were out of stock: "
+str(tracker.notInStock))
send.sending()


tracker.inStock.clear()