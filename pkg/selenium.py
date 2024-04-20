import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class Selenium:
  def __init__(self) -> None:
    os.environ['CHROMEDRIVER'] = '~/Downloads/chrome-mac-arm64/chrome_driver.app'
    # self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    options = Options()
    options.add_argument("--headless=new")
    self.driver = webdriver.Chrome(options=options)

  def login(self, user, password):
    self.driver.get('https://www.linkedin.com/login')
    self.driver.find_element(By.ID, 'username').send_keys(user)
    self.driver.find_element(By.ID, 'password').send_keys(password)
    self.driver.find_element(By.CSS_SELECTOR, '.login__form_action_container button').click()

  def scroll_to_bottom(self):
    start = time.time()
    initialScroll = 0
    finalScroll = 1000
    
    while True:
      self.driver.execute_script(f"window.scrollTo({initialScroll}, {finalScroll}) ")
      initialScroll = finalScroll
      finalScroll += 1000

      time.sleep(3)

      end = time.time()

      if round(end - start) > 5:
        break
  
  def set_page_source(self, url):
    self.driver.get(url)
    self.scroll_to_bottom()
    page_source = self.driver.page_source

    self.soup = BeautifulSoup(page_source, 'html.parser')

  def get_profile(self):
    name = self.soup.find('div', {'class': 'artdeco-entity-lockup__title ember-view'}).text.strip()
    headline = self.soup.find('div', {'class': 'artdeco-entity-lockup__subtitle ember-view truncate'}).text.strip()

    return {
      'name': name,
      'headline': headline
    }
  
  def get_about(self):
    try:
      about = self.soup.find('div', {'class': 'display-flex ph5 pv3'}).find('span')
      return about.text.strip()
    except:
      return None

  def get_experience(self):
    experience = self.soup.find('div', {'class': 'pvs-list__outer-container'})

    sections = self.soup.find_all('section', class_=['artdeco-card', 'pv-profile-card', 'break-words', 'mt2'], attrs={'tabindex': '-1', 'data-view-name': 'profile-card'})

    experience = None
    for section in sections:
      if section.find('div', id='experience'):
        experience = section.text.strip().replace('\n', '')

    return experience

