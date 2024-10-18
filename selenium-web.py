from selenium import webdriver

class Info:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

    def get_info(self, query):
        self.query = query
        self.driver.get(url="https://www.google.com")
        search = self.driver.find_element_by_xpath('/html/body/div[1]/div[3]')
        

# Usage example
assist = Info()
assist.get_info("hello")
