import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import warnings


class ll_ATS(unittest.TestCase):
    #set up the test class - assign the driver to Chrome - if using a different
    #browser, change the browser name below
    def setUp(self):
        self.driver = webdriver.Chrome()
        warnings.simplefilter('ignore', ResourceWarning) #ignore resource warning if occurs

    # If login is successful, 'Logout' will be displayed as the text in the Navbar
    def test_ll(self):
        user = "ayuni"       #must be a valid username for the application
        pwd = "Morgoth7!"         #must be the password for a valid user

        #open the browser and go to the admin page
        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000/admin")

        #find the username and password input boxes on the screen by ID
        #send the username and password to each box
        #send the Return (Enter) key to the system
        #go to the main application page
        elem = driver.find_element(By.ID, "id_username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID, "id_password")
        elem.send_keys(pwd)
        time.sleep(3)
        elem.send_keys(Keys.RETURN)
        time.sleep(3)
        driver.get("http://127.0.0.1:8000")
        time.sleep(3)


        #if the Logout Link Text is found on the screen
        #   assert "Logged in" is True
        try:
           elem = driver.find_element(By.LINK_TEXT, "| LogOut |")
           print("Test Passed - Valid user logs in and logs out sucessfully")
           assert True

        #else report that the test failed
        except NoSuchElementException:
            self.fail("Test Passed - Valid user logs in and logs out sucessfully")

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
