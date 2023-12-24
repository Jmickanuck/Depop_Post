from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time 
import pyautogui
from fake_useragent import UserAgent
#setTimeout (() => {debugger;} ,3000)

Error = False #Check for User Input Errors

class Pop_Driver:
    options = Options()
    options.add_experimental_option("detach", True)

    options.add_argument('--start-maximized')
    ua = UserAgent()
    random_user_agent = ua.random
    options.add_argument(f'user-agent={random_user_agent}')
    options.add_argument('--start-maximized')
    options.add_argument('--headless')

    def __init__(self, *args, **kwargs):
        
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)

        self.wait = WebDriverWait(self.driver, 10)
        self.Login(**kwargs)
        time.sleep(2)
        self.Description(**kwargs)
        self.driver.execute_script("window.scrollTo(0, 600)")
        self.Info_Cat(**kwargs)
        self.Sub_Cat(**kwargs)
        self.Brand(**kwargs)
        self.Condition(**kwargs)
        print('Done')
        time.sleep(2)

    def Login(self, **kwargs):
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.driver.get('https://www.depop.com/login/')  # Go to Depop Login Page

        self.driver.find_element_by_xpath('//*[@id="__next"]/div/div[3]/div[2]/button[2]').click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(self.username) # Enter Username
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'password'))).send_keys(self.password) # Enter Password
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div[4]/form/button'))).click() # Click Login

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mainNavigation"]/li[2]/a/button'))).click() #Click Sell
        
    def Description(self, **kwargs):
        self.description = kwargs.get('desc')
        self.driver.execute_script("window.scrollTo(0, 200)") #Scroll to Description
        self.driver.find_element_by_id('description').send_keys(self.description) 
            
    def Info_Cat(self, **kwargs):
        self.category = kwargs.get('category')
        self.type = kwargs.get('type')
        self.driver.find_element_by_xpath('//*[@id="listingCategories__category__select"]').click()
        time.sleep(1) #Wait for Category to load
        
        if self.type == 'm': #Select Category MALE
                categories = ['t', 'b', 'c', 'j','s','f','a','sw','u','swim','cost']  # List of categories
                self.Cat_Picker(self, *categories, category = self.category)
                        
        elif self.type == 'f': #Select Category FEMALE
                categories = ['t', 'b','d','c', 'j','s','f','a','sw','u','swim','cost']  # List of categories
                dropdown = self.driver.find_element_by_xpath('//*[@id="listingCategories__category__select"]')  # replace with the actual XPath
                for _ in range(11):
                    dropdown.send_keys(Keys.ARROW_DOWN)
                    time.sleep(0.05)
                self.Cat_Picker(self, *categories, category = self.category)
                    

        else:
                Error = True
                
    def Cat_Picker(self,*args, **kwargs):
        self.category = kwargs.get('category')
        self.categories = args
        dropdown = self.driver.find_element_by_xpath('//*[@id="listingCategories__category__select"]')  # replace with the actual XPath
        for index, cat in list(args):
            if self.category == cat:
                for _ in range(index):
                    dropdown.send_keys(Keys.ARROW_DOWN)
                    time.sleep(0.05)
                dropdown.send_keys(Keys.ENTER)
                break
    def Sub_Cat(self, **kwargs):
        self.category_dict = {
            't': {'t': 't-shirts', 'h': 'hoodies', 'sws': 'sweatshirts', 's': 'sweaters', 'c': 'cardigans', 'sh': 'shirts', 'ps': 'Polo', 'bl': 'blouse ', 'ct': 'crop', 'tnk': 'tank tops', 'co': 'corsets', 'bs': 'bodysuits', 'o': 'other'},
            'b': {'j': 'jeans', 'p': 'pants', 's': 'shorts', 'sk': 'skirts', 'sp': 'sweatpants', 'l': 'leggings', 'o': 'other'},
            'c': {'c': 'coats', 'j': 'jackets', 'v': 'vests', 'o': 'other'},
            'j': {'j': 'jumpsuits', 'r': 'rompers','ov':'overalls', 'o': 'other'},
            's': {'s': 'suits', 'tj': 'tailored jackets', 'tt': 'tailored trousers','v':'vests', 'o': 'other','tux': 'tuxedo'},
            'a': {'b':'bags','bl': 'belts', 'h': 'hats', 'g': 'gloves', 'sc': 'scarves', 's': 'sunglasses', 'wl': 'watches', 'j': 'jewellery', 'hr': 'hair accessories','wl':'wallet', 'o': 'other'},
            'u': {'bd': 'bandeaus', 's': 'socks', 'o': 'other', 'us': 'undershirts', 'br': 'bras', 'p': 'panties', 'sw': 'shapewear', 'bb': 'boxers', 't': 'tights'}
        }
        self.Sub_Cat_Picker(**kwargs)

    def Sub_Cat_Picker(self, **kwargs):
        self.category = kwargs.get('category')
        self.sub_category = kwargs.get('subcat')
        for cat in self.category_dict:
            if cat == self.category:
                for sub_cat in self.category_dict[cat]:
                    if sub_cat == self.sub_category:
                        input_field = self.driver.find_element_by_xpath('//*[@id="listingCategories__subcategory__select"]')
                        input_field.send_keys(self.category_dict[cat][sub_cat])
                        input_field.send_keys(Keys.ENTER)
                        break
            else:
                self.driver.find_element_by_xpath('//*[@id="listingCategories__subcategory__select"]').send_keys(Keys.DELETE)
                break
    def Brand(self, **kwargs):
        self.brand = kwargs.get('brand')
        self.driver.find_element_by_xpath('//*[@id="main"]/form/div[4]/div[3]/div/div/div[1]').click()
        input_field = self.driver.find_element_by_xpath('//*[@id="listingBrands__select"]')  # replace with the actual XPath
        input_field.send_keys(self.brand)
        input_field.send_keys(Keys.ENTER)

    def Condition(self, **kwargs):
        self.condition = kwargs.get('condition')
        Condition_Dict = {1: 'Brand New', 2: 'Like New', 3: 'Used - E', 4: 'Used - G', 5: 'Used - F'}
        xpath_str = '//*[@id="listingSelect__listing__condition__select"]'
        xpath = self.driver.find_element_by_xpath('//*[@id="listingSelect__listing__condition__select"]').click()
        self.DropDown(Condition_Dict, self.condition, xpath_str)

    def DropDown(self, arg1, arg2, arg3):
        Dict = arg1
        Type = arg2
        xpath = arg3

        for key in Dict:
            if key == Type:
                input_field = self.driver.find_element_by_xpath(xpath)
                input_field.send_keys(str(Dict[key]))
                input_field.send_keys(Keys.ENTER)
                break
        
        
        
#Login('MickNuck','Lewandowski56!')

Pop_Driver(username = 'MickNuck',password = 'Lewandowski56!', desc = 'This is a test description', type = 'f', category = 'u', subcat = 'sw', brand = 'Monki', condition = 1)