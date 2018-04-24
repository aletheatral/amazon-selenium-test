import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


CONFIGS = {"Driver": webdriver.Chrome(),
           "URL": "https://www.amazon.com",
           "username": "amazontestuser23@gmail.com",
           "password": "Amazontest",
           "search_key": "samsung"}


VAR = {"data_asin": "",
       "item": ""}


class AmazonTest:

    def __init__(self):

        self.driver = CONFIGS["Driver"]
        self.URL = CONFIGS["URL"]
        self.user = CONFIGS["username"]
        self.password = CONFIGS["password"]
        self.search_key = CONFIGS["search_key"]
        self.Is_loggedin = False
        self.Is_search_result = False
        self.Is_page = False
        self.Is_item_page = False
        self.is_aria_hidden = True
        self.Is_list = False
        self.Is_inList = False
        self.Is_delItem = False
        self.Is_checkDel = False

    def getPage(self):

        self.driver.get(self.URL)
        self.driver.maximize_window()
        self.current_url = self.driver.current_url
        print self.current_url

        return self.current_url

    def signIn(self):

        self.nav_account_list = self.driver.find_element_by_id(
            "nav-link-accountList").click()

        self.user_input = self.driver.find_element_by_id("ap_email")
        self.user_input.send_keys(self.user)
        self.continue_button = self.driver.find_element_by_id("continue")
        self.continue_button.click()

        self.pass_input = self.driver.find_element_by_id("ap_password")
        self.pass_input.send_keys(self.password)
        self.submit_button = self.driver.find_element_by_id("signInSubmit")
        self.submit_button.click()

        self.Is_loggedin = True
        return self.Is_loggedin

    def search(self):

        search_box_id = "twotabsearchtextbox"
        self.search_input = self.driver.find_element_by_id(search_box_id)
        self.search_input.click()
        self.search_input.send_keys(self.search_key)
        self.search_button = self.driver.find_element_by_class_name(
            "nav-input")
        self.search_button.click()

        self.search_results = self.driver.find_element_by_id("s-result-count")

        if self.search_results:
            self.Is_search_result = True
        return self.Is_search_result

    def goPage(self):

        page_path = "//*[@id='pagn']/span[3]/a"
        self.secondPage = self.driver.find_element_by_xpath(page_path)
        self.secondPage.click()

        if "page=2" in self.driver.current_url:
            self.Is_page = True
        return self.Is_page

    def selectItem(self):

        self.item = self.driver.find_element_by_css_selector(
            "#s-results-list-atf li:nth-of-type(3)")
        VAR["data_asin"] = self.item.get_attribute("data-asin")
        self.item_link = self.item.find_element_by_tag_name("img")
        self.item_link.click()

        self.Is_item_page = True
        return self.Is_item_page

    def addList(self):

        self.add_to_WL_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, "add-to-wishlist-button-submit")))
        self.add_to_WL_button.click()
        self.WL_result_modal = self.driver.find_element_by_id("a-popover-7")
        self.Is_aria_hidden = self.WL_result_modal.get_attribute("aria-hidden")

        self.continue_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "WLHUC_continue")))
        self.continue_button.click()

        return self.Is_aria_hidden

    def goList(self):

        self.account_list = self.driver.find_element_by_id(
            "nav-link-accountList")
        ActionChains(self.driver).move_to_element(self.account_list).perform()

        self.WL_link = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "nav-flyout-wl-items")))
    
        self.WL_link.click()

        self.Is_list = True
        return self.Is_list

    def checkList(self):

        self.WL = self.driver.find_element_by_id("g-items")
        self.WL_items = self.WL.find_elements_by_tag_name("div")

        for item in self.WL_items:
            params = item.get_attribute("data-reposition-action-params")
            if VAR["data_asin"] in params:
                VAR["item"] = item
                self.Is_inList = True
                return self.Is_inList
        return self.Is_inList

    def delItem(self):

        VAR["item"].find_element_by_xpath(
            "//a[contains(text(), 'Delete item')]").click()
        self.Is_delItem = True
        return self.Is_delItem

    def checkDelItem(self):

        try:
            self.WL = self.driver.find_element_by_id("g-items")
            self.WL_items = self.WL.find_elements_by_tag_name("div")

            for item in self.WL_items:
                del_alert = item.find_element_by_xpath(
                    "//div[contains(text(), 'Deleted')]")
                if del_alert:
                    self.Is_checkDel = True
                    return self.Is_checkDel

        except NoSuchElementException:
            self.Is_checkDel = True
        return self.Is_checkDel

    def destroyDriver(self):

        self.driver.close()


class TestAmazonTest:

    def test_getPage(self):

        amazon_class_instance = AmazonTest()
        assert amazon_class_instance.getPage() == "https://www.amazon.com/"

    def test_signIn(self):

        amazon_class_instance = AmazonTest()
        amazon_class_instance.signIn()
        assert amazon_class_instance.Is_loggedin == True

    def test_search(self):

        amazon_class_instance = AmazonTest()
        amazon_class_instance.search()
        assert amazon_class_instance.Is_search_result == True

    def test_goPage(self):

        amazon_class_instance = AmazonTest()
        amazon_class_instance.goPage()
        assert amazon_class_instance.Is_page == True

    def test_selectItem(self):

        amazon_class_instance = AmazonTest()
        amazon_class_instance.selectItem()
        assert amazon_class_instance.Is_item_page == True

    def test_addList(self):

        amazon_class_instance = AmazonTest()
        amazon_class_instance.addList()
        assert amazon_class_instance.Is_aria_hidden == "false"

    def test_goList(self):

        amazon_class_instance = AmazonTest()
        amazon_class_instance.goList()
        assert amazon_class_instance.Is_list == True

    def test_checkList(self):

        amazon_class_instance = AmazonTest()
        amazon_class_instance.checkList()
        assert amazon_class_instance.Is_inList == True

    def test_delItem(self):

        amazon_class_instance = AmazonTest()
        amazon_class_instance.delItem()
        assert amazon_class_instance.Is_delItem == True

    def test_checkDelItem(self):

        amazon_class_instance = AmazonTest()
        amazon_class_instance.checkDelItem()
        amazon_class_instance.destroyDriver()
        assert amazon_class_instance.Is_checkDel == True
