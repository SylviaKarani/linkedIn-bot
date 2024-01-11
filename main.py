from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time, random
import pyautogui
from itertools import product


class LinkedInBot:
    def __init__(self, parameters):
        self.email = parameters['email']
        self.password = parameters['password']
        self.disable_lock = parameters['disableAntiLock']
        self.positions = parameters.get('positions', [])
        self.locations = parameters.get('locations', [])
        self.base_search_url = self.get_base_search_url(parameters)
        
        chrome_driver_path = ChromeDriverManager().install()
        service = Service(executable_path= chrome_driver_path)
        
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features")
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless") 
        
        
        
        self.driver = webdriver.Chrome(service=service, options=options)
     

    def login(self):
        try:
            self.driver.set_window_size(1200, 800)
            
            
            self.driver.get("https://www.linkedin.com/login")
            time.sleep(random.uniform(5, 10))
            self.driver.find_element(By.ID, "username").send_keys(self.email)
            self.driver.find_element(By.ID, "password").send_keys(self.password)
            self.driver.find_element(By.CSS_SELECTOR,".btn__primary--large").click()
            time.sleep(random.uniform(5, 10))
            
            print("Login button Clicked!")
            
            # Check for security check after pressing login button
            self.security_check()
            
            
            # Use WebDriverWait to wait for the presence of an element after successful login
            WebDriverWait(self.driver, 20).until(
                EC.url_matches("https://www.linkedin.com/feed/")
            )

            print("Login successful!")
            
            self.driver.save_screenshot('after_login.png')
            print("Screenshot saved!")
            
        except TimeoutException as te:
            print(f"TimeoutException: {te}")
            raise Exception("Could Not Log In!")
         

        except Exception as e:
            print(f"Exception: {e}")
            raise Exception("An unexpected error occurred during login!")
        self.driver.save_screenshot('after_login.png')  
    
    
    def security_check(self):
        current_url = self.driver.current_url
        page_source = self.driver.page_source

        if '/checkpoint/challenge/' in current_url or 'security check' in page_source:
            print(f"Security check detected.")
            input("Press Enter in this console when the security check is done.")
            time.sleep(random.uniform(5.5, 10.5))
     
            
    def apply_filters(self):
        try:
            print("CLicking Jobs button")
            time.sleep(random.uniform(5, 10))
            # Click on the "Jobs" button to go to the Jobs section
            jobs_button = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@href='https://www.linkedin.com/jobs/?']"))
                )
            jobs_button.click()
            
            print("In Job Page")
            time.sleep(random.uniform(5, 10))
            self.driver.save_screenshot('job_page.png')
            

            # Input job title
            title_input = WebDriverWait(self.driver, 40).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']")))
            time.sleep(random.uniform(5, 10))
            
            
            title_input.send_keys(self.positions[0])
            print("entered job title")
            
            title_input.send_keys(Keys.RETURN)
            # After pressing Enter
            self.driver.save_screenshot("entered_job_search.png")
            
            print("Input search value and pressed enter")
            
            # Get the base search URL
            search_url = self.get_base_search_url(parameters)
            self.driver.get(search_url)

            
            # Wait for the search page to load
            WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.jobs-search-results-list"))
            )

            # Capture screenshot after the search results have loaded
            self.driver.save_screenshot('after_search.png')
            print("Screenshot saved!")
            
            time.sleep(random.uniform(20, 20))
            
            # Apply filters based on user preferences
            self.apply_easy_apply_filter()
            self.apply_other_filters(parameters)
            
        except TimeoutException as te:
            print(f"TimeoutException: {te}")
            print(f"Current URL: {self.driver.current_url}")
            raise Exception("An unexpected error occurred while applying filters.")
        except Exception as e:
            print(f"Exception: {e}")
            raise Exception("An unexpected error occurred while applying filters.")
             
    def apply_date_posted_filter(self, option):
        time.sleep(random.uniform(15, 20)) 
        
        if option:
            date_posted_button = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable((By.ID, "searchFilter_timePostedRange"))
            )
            date_posted_button.click()
            print("Date Posted button clicked")
        
            time.sleep(random.uniform(10, 20))
            self.driver.save_screenshot("dateposted clicked.png")
        
            time.sleep(random.uniform(5, 10))

            # Select the desired option
            option_span = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[text()='{option}']"))
            )
            option_span.click()
            print(f"Option '{option}' selected")
            self.driver.save_screenshot("option_selected_date.png")
        
            time.sleep(random.uniform(10, 20))
            self.driver.save_screenshot("option_selected_date.png")
        
        # Click "Show results" button
        self.click_show_results_button()
                         
    def apply_company_filter(self, company_name):
        time.sleep(random.uniform(5, 10))
        
        if company_name:
            company_button = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable((By.ID, "searchFilter_company"))
                )
            company_button.click()
            print("Company button clicked")
            
            time.sleep(random.uniform(10,20))
            self.driver.save_screenshot("company_filter.png")
            
            time.sleep(random.uniform(5,10))
            
            # Input company name
            company_input = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='company-filter-value']"))
                )
            company_input.send_keys(company_name)
            print(f"Company {company_name} inputed")
            self.driver.save_screenshot("company_searched.png")
            
            time.sleep(random.uniform(10, 20))
            self.driver.save_screenshot("company_name_selected.png")
            
        # Click "Show results" button
        self.click_show_results_button()
            
    def apply_experience_filter(self, experience_levels):
        time.sleep(random.uniform(5, 10)) 
        
        if experience_levels:
            experience_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.ID, "searchFilter_experience"))
                )
            experience_button.click()
            print("Experience button clicked")
            
            time.sleep(random.uniform(10, 20))
            self.driver.save_screenshot("experience_clicked.png")
        
            time.sleep(random.uniform(5, 10))
            
            for level in experience_levels:
                # Input experience level
                experience_input = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, f"//span[text()='{level}']"))
                    )
                experience_input.click()
                print(f" '{level}' selected")
                
                self.driver.save_screenshot("experience_selected.png")
        
                time.sleep(random.uniform(10, 20))
                self.driver.save_screenshot("experience_selected.png")
               
        time.sleep(random.uniform(20, 30))
        # Click "Show results" button
        self.click_show_results_button()
                    
    def apply_remote_filter(self, remote_options):
        time.sleep(random.uniform(5, 10)) 
        
        if remote_options:
            remote_button = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable((By.ID, "searchFilter_workplaceType"))
                )
            remote_button.click()
            
            print("Remote button clicked")
        
            time.sleep(random.uniform(10, 20))
            self.driver.save_screenshot("remote clicked.png")
        
            time.sleep(random.uniform(5, 10))
            
            for option in remote_options:
                # Input remote option
                remote_input = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, f"//span[text()='{option}']"))
                    )
                remote_input.click()
                print(f"'{option}' selected")
                self.driver.save_screenshot("remote.png")
        
                time.sleep(random.uniform(10, 20))
                self.driver.save_screenshot("remote.png")
                
        # Click "Show results" button
        self.click_show_results_button()
    
    def apply_other_filters(self, parameters):
        try:
            
            # Check if Easy Apply is the only filter specified
            only_easy_apply = (
                'experience_levels' not in parameters
                and 'date_posted' not in parameters
                and 'company' not in parameters
                and 'remote_options' not in parameters
                and parameters.get('easy_apply', False)  # Check if Easy Apply is True
                )
            
            if not only_easy_apply:
                # Apply experience filter if 'experience_levels' parameter is present
                if 'experience_levels' in parameters:
                    self.apply_experience_filter(parameters['experience_levels'])

                # Apply date posted filter if 'date_posted' parameter is present
                date_posted_applied = False
                if 'date_posted' in parameters and not date_posted_applied:
                    self.apply_date_posted_filter(parameters['date_posted'])
                    date_posted_applied = True

                # Apply company filter if 'company' parameter is present
                if 'company' in parameters:
                    self.apply_company_filter(parameters['company'])

                # Apply remote filter if 'remote_options' parameter is present
                if 'remote_options' in parameters:
                    self.apply_remote_filter(parameters['remote_options'])
                
                self.driver.save_screenshot("Selecting_Filters.png")
            
                # Clicking the "Show results" button
                self.click_show_results_button()
                self.driver.save_screenshot("Search_results.png")
            
                time.sleep(random.uniform(30, 50))
                self.driver.save_screenshot("search_results.png")
                print("Search Results")
            
        except TimeoutException as te:
            print(f"TimeoutException: {te}")
            print(f"Current URL: {self.driver.current_url}")
            raise Exception("An unexpected error occurred while applying other filters.")
        except Exception as e:
            print(f"Exception: {e}")
            raise Exception("An unexpected error occurred while applying other filters.")           
    
    def apply_easy_apply_filter(self):
        time.sleep(random.uniform(20, 30))
        try:
            # Check if the "Easy Apply" button is already enabled
            easy_apply_button = self.driver.find_element(By.XPATH, "//button[@aria-label='Easy Apply filter.']")
            time.sleep(random.uniform(20, 30))
            
            # Check if the button has the "aria-checked" attribute set to "false"
            if easy_apply_button.get_attribute('aria-checked') == 'false':
                # Clicking the "Easy Apply" button to enable it
                easy_apply_button.click()
                time.sleep(random.uniform(20, 30))

                # Wait for the page to reload with Easy Apply jobs
                WebDriverWait(self.driver, 100).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.jobs-search-results-list"))
                )
                time.sleep(random.uniform(20, 30))
                print("Wait page to reload")
                self.driver.save_screenshot("EasyApply_button.png")
                
            else:
                print("Easy Apply button is already enabled.")
                self.driver.save_screenshot("EasyApply_button.png")
                time.sleep(random.uniform(20, 30))
                 

        except NoSuchElementException:
            print("Easy Apply button not found.")
        except TimeoutException as te:
            print(f"TimeoutException: {te}")
            raise Exception("Timed out waiting for Easy Apply jobs.")
        except Exception as e:
            print(f"Exception: {e}")
            raise Exception("An unexpected error occurred while applying Easy Apply filter.")
           
    def apply_radio_filter(self, filter_name, selected):
        # Click on a radio button filter
        if selected:
            radio_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, f"//label[text()='{filter_name}']/preceding-sibling::input[@type='radio']"))
                )
            radio_button.click()

    def apply_checkbox_filters(self, filter_name, values):
        # Click on checkbox filters
        for value in values:
            checkbox = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f"input[name='{filter_name}'][value='{str(value)}']"))
            )
            checkbox.click()
    
    def click_show_results_button(self):
        try:
            # Assuming the "Show results" button has a unique identifier or XPath
            time.sleep(random.uniform(20, 30))
            print("pressing show results button") 
            self.driver.save_screenshot("pressingshowbutton.png")
            
            time.sleep(random.uniform(20, 30))  
            self.driver.save_screenshot("pressingshowbutton.png")
            
            
            time.sleep(random.uniform(5, 10))
            show_results_button = WebDriverWait(self.driver, 100).until(
               EC.element_to_be_clickable((By.XPATH, "//button[@data-control-name='filter_show_results']"))
            )
            time.sleep(random.uniform(5, 10))
            
            print("Found 'Show results' button, attempting to click...")
            show_results_button.click()
            print("show results button clicked")
            
            time.sleep(random.uniform(20, 30))
            self.driver.save_screenshot("showbuttonclicked.png")
            
            time.sleep(random.uniform(20, 30))
            self.driver.save_screenshot("showbuttonclicked.png")

            # Wait for either search results or no matching jobs found message
            print("wait for search result...")
            WebDriverWait(self.driver, 120).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.jobs-search-results-list, div.jobs-search-no-results-banner"))
            )

            
            # Check if search results are present
            print("Checking if there are results")
            if self.driver.find_elements(By.CSS_SELECTOR, "div.jobs-search-results-list"):
                search_results_url = self.driver.current_url
                print(f"Search Results URL: {search_results_url}")
                
                time.sleep(random.uniform(10, 20))
                self.driver.save_screenshot('search_results.png')
                
                time.sleep(random.uniform(10, 20))
                self.driver.save_screenshot('search_results.png')
                print("Screenshot saved!")
            else:
                # Handle the case where no matching jobs are found
                print("No matching jobs found. Clearing filters...")
                self.clear_all_filters()
        

        except TimeoutException as te:
            print(f"TimeoutException: {te}")
            raise Exception(f"Timed out waiting for search results. Original exception: {te}")
        except Exception as e:
            print(f"Exception: {e}")
            raise Exception(f"An unexpected error occurred while clicking 'Show results' button. Original exception: {e}")

    def clear_all_filters(self):
        try:
            clear_filters_button = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Clear all filters']"))
            )
            clear_filters_button.click()
            print("Cleared all filters.")
        except TimeoutException:
            print("TimeoutException: Clear filters button not found.")
        except Exception as e:
            print(f"Exception: {e}")
            raise Exception("An unexpected error occurred while clearing filters.")
        
    def get_base_search_url(self, parameters):
        remote_url = ""
        
        if parameters.get('remote'):
            remote_url = "&f_CF=f_WRA"

        level = 1
        experience_level = parameters.get('experienceLevel', [])
        experience_url = "&f_E="
        
        for level in experience_level:
                experience_url += "%2C" + str(level)
                level += 1

        distance_url = f"?distance={parameters.get('distance', 25)}"

        job_types_url = "&f_JT="
        job_types = parameters.get('experienceLevel', [])
        for key in job_types:
            if job_types[key]:
                job_types_url += "%2C" + key[0].upper()

        date_url = ""
        dates = {"all time": "", "month": "&f_TPR=r2592000", "week": "&f_TPR=r604800", "24 hours": "&f_TPR=r86400"}
        date_table = parameters.get('date', [])
        for key in date_table:
            if date_table[key]:
                date_url = dates[key]
                break

        easy_apply_url = "&f_LF=f_AL"
        
        extra_search_terms = [distance_url, remote_url, job_types_url, experience_url]
        extra_search_terms_str = ''.join(term for term in extra_search_terms if len(term) > 0) + easy_apply_url + date_url
        return f"https://www.linkedin.com/jobs/search/{extra_search_terms_str}&origin=JOBS_HOME_SEARCH_BUTTON&refresh=true"
           
    def logout(self):
        pass
    def close(self):
        self.driver.quit()



parameters = {
    'email': 'gassuntamal2@gmail.com',
    'password': 'Bot12345678',
    'disableAntiLock': True,
    'positions': ['engineer'],
    'locations': ['San Francisco'],
    'easy_apply': True,
    #'experience_levels': ['Entry level'],
    #'job_types': ['Full-time', 'Part-time'],
    'date_posted': 'Any time',  
    #'company': 'Example Company',  
    #'remote_options': ['Remote', 'Hybrid'],
}


bot = LinkedInBot(parameters)

print("Initialized LinkedInBot")

try: 
    bot.login()
    print("Login completed")
    bot.apply_filters()
    print("Started APllying Process")
    
finally:
    bot.close()
    print("Script completed")

