import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

class TabelogLiker:
    def __init__(self, remote_debugging_port=9222):
        """
        Args:
            remote_debugging_port: Port for remote debugging (default: 9222)
        """
        self.base_url = "https://tabelog.com"
        self.mypage_url = "https://tabelog.com/rvwr/000141867"
        self.driver = None
        self.wait = None
        self.remote_debugging_port = remote_debugging_port
        
    def connect_to_existing_browser(self):
        """Connect to an existing Chrome browser instance with remote debugging enabled"""
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{self.remote_debugging_port}")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 20)
            return True
        except Exception as e:
            print(f"Failed to connect to existing browser: {e}")
            return False
        
    def setup_driver(self):
        chrome_options = Options()
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)

    def click_follow_button(self):
        follow_button = self.driver.find_element(By.CLASS_NAME, "p-follow-btn__target")
        has_is_added = "is-added" in follow_button.get_attribute("class").split()
        if not has_is_added:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", follow_button)
            time.sleep(1)
            if follow_button.is_displayed() and follow_button.is_enabled():
                follow_button.click()
                time.sleep(1)
    
    def click_like_button_for_liker(self, full_url):
        self.driver.get(full_url)
        try:
            rvw_items_present = self.wait.until(lambda d: d.find_elements(By.CLASS_NAME, "rvw-item"))
        except Exception:
            self.click_follow_button()
            return
        if not rvw_items_present:
            self.click_follow_button()
            return

        self.click_follow_button()

        rvw_items = self.driver.find_elements(By.CLASS_NAME, "rvw-item")
        limited_rvw_items = rvw_items[:10]
        for rvw_item in limited_rvw_items:
            try:
                like_btn_div = rvw_item.find_element(By.CLASS_NAME, "like-btn")
                like_button = like_btn_div.find_element(By.CLASS_NAME, "like-btn__label")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", like_button)
                time.sleep(1)
                if like_button.is_displayed() and like_button.is_enabled():
                    like_button.click()
                    time.sleep(1)
            except Exception:
                continue
    
    def get_likers(self):
        self.driver.get(self.mypage_url)
        time.sleep(1)

        my_rvw_items = self.driver.find_elements(By.CLASS_NAME, "rvw-item")
        limited_my_rvw_items = my_rvw_items[:10]

        data_urls = []
        for my_rvw_item in limited_my_rvw_items:
            try:
                like_btn_div = my_rvw_item.find_element(By.CLASS_NAME, "like-btn")
                like_count_btn = like_btn_div.find_element(By.CLASS_NAME, "like-btn__count")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", like_count_btn)
                time.sleep(1)
                if like_count_btn.is_displayed():
                    like_count_btn.click()
                    time.sleep(2)
                    like_users_listview = self.driver.find_element(By.ID, "like-users-listview")
                    like_users = self.driver.find_elements(By.CLASS_NAME, "p-modal-like__item")
                    for like_user in like_users:
                        a_tag = like_user.find_element(By.CLASS_NAME, "p-modal-like__target")
                        data_url = a_tag.get_attribute("href")
                        if not data_url:
                            continue
                        data_urls.append(data_url)
                    body = self.driver.find_element(By.TAG_NAME, "body")
                    actions = ActionChains(self.driver)
                    actions.move_to_element_with_offset(body, 200, 200).click().perform()
                    time.sleep(1)
            except Exception:
                continue

        for idx, data_url in enumerate(data_urls, start=1):
            print(f"Processing liker #{idx}: {data_url}")
            self.click_like_button_for_liker(data_url)
            time.sleep(2)
    
    def run(self):
        try:
            print("Starting Tabelog Liker...")
            
            # Connect to existing browser
            if not self.connect_to_existing_browser():
                self.setup_driver()
                input("Press Enter after you've logged in and navigated to the your tabelog page...")
            
            self.get_likers()
            
        except KeyboardInterrupt:
            print("Interrupted by user")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract like elements from Tabelog my page")
    parser.add_argument("--remote-port", type=int, default=9222, help="Remote debugging port (default: 9222)")
    
    args = parser.parse_args()
    
    tabelog_liker = TabelogLiker(remote_debugging_port=args.remote_port)
    likers = tabelog_liker.run()