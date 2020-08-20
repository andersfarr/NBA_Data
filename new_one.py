import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import lxml
import time
import os
driver = webdriver.Chrome('chromedriver.exe')
nba_teams = ['Atlanta Hawks','Boston Celtics','Brooklyn Nets','Charlotte Hornets','Chicago Bulls','Cleveland Cavaliers','Dallas Mavericks','Denver Nuggets','Detroit Pistons','Golden State Warriors','Houston Rockets','Indiana Pacers','Los Angeles Clippers','Los Angeles Lakers','Memphis Grizzlies','Miami Heat','Milwaukee Bucks','Minnesota Timberwolves','New Orleans Pelicans','New York Knicks','Oklahoma City Thunder','Orlando Magic','Philadelphia 76ers','Phoenix Suns','Portland Trail Blazers','Sacramento Kings','San Antonio Spurs','Toronto Raptors','Utah Jazz','Washington Wizards']
team_pages = np.array([])

def wait_for(condition_function, cond_input):
    start_time = time.time()
    while time.time() < start_time + 3:
      if condition_function(cond_input):
        return True
      else:
        time.sleep(0.1)
    raise Exception(
     'Timeout'
    )
def link_has_gone_stale_id(element_id):
    try:
      # poll the link with an arbitrary call
      link.find_elements_by_id('element_id')
      return False
    except:
      return True

def link_has_gone_stale_link(element_id):
    try:
      # poll the link with an arbitrary call
      link.find_elements_by_link('element_id')
      return False
    except:
      return True

def click_through_to_new_page(link_text):
  link = driver.find_element_by_link_text(link_text)
  driver.execute_script("arguments[0].scrollIntoView();", link)
  time.sleep(0.2)
#  driver.execute_script("scroll(0,200)")
#  time.sleep(0.2)
  link = driver.find_element_by_link_text(link_text)
  link.click()
  wait_for(link_has_gone_stale_id,'team_ws_images_link')

def get_team_data():
    time.sleep(4)
    table = driver.find_element_by_xpath("/html/body/div[2]/div[5]/div[3]/div[2]/div/table")
    df = pd.read_html(table.get_attribute('outerHTML'))
    return df

dir = "C:\\Users\\afarr\\OneDrive - Intel Corporation\\Desktop\\Python\\NBA_data"
if not os.path.exists(dir):
    os.mkdir(dir)
for team in nba_teams:
  print(team)
  driver.get('https://www.basketball-reference.com/teams')
  wait_for(link_has_gone_stale_link, team)
  click_through_to_new_page(team)
  df = get_team_data()
  print(df)
  new_df =  df[0]
  dir = "C:\\Users\\afarr\\OneDrive - Intel Corporation\\Desktop\\Python\\NBA_data"
  dir = dir + "\\" + team
  if not os.path.exists(dir):
      os.mkdir(dir)
  new_df.to_csv(dir + "\\team_hist.csv")



driver.close()
