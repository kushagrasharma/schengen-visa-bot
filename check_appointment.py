import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import dateutil.parser as dparser
import datetime
import os

def login():
    driver = webdriver.Firefox()
    driver.get("https://pastel.diplomatie.gouv.fr/rdvinternet/html-3.04.03/frameset/frameset.html?lcid=1&sgid=260&suid=1")
    driver.switch_to.frame(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "BODY_WIN"))))
    sleep(5)
    driver.execute_script("parent.parent.ComposantMenuFrameset.SelectItem2Menu1(0,0,false)")
    driver.switch_to.frame(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "CONTENU_WIN"))))

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ccg"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "boutonSuivant"))).click()
    #driver.execute_script("tabElementForm[0].suivant()")
    return driver
    #login = driver.find_element_by_class_name("menu1Item2")
    #login.click()
    #driver.find_element_by_id("boutonSuivant_link")
    #driver.click()
    #sleep(5)
    #driver.close()



def is_valid_appt(driver):
    print(driver.find_element_by_id("compTableau_Entete").text)
    d = dparser.parse(driver.find_element_by_id("compTableau_Entete").text)
    print(d)
    return datetime.date.today() <= d <= datetime.date(2016, 8, 1)


def check_for_appts():
    try:
        driver = login()
        while True:
            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                           'Timed out waiting for PA creation ' +
                                           'confirmation popup to appear.')

                alert = driver.switch_to_alert()
                alert.accept()
                print("alert accepted")
            except TimeoutException:
                if is_valid_appt(driver):
                    os.system('say "an appointment has been found hella sick"')
                    input("Press ENTER to continue.")
            sleep(30)
            driver.refresh()
            driver.switch_to.frame(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "BODY_WIN"))))
            driver.switch_to.frame(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "CONTENU_WIN"))))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "boutonSuivant"))).click()
    except TimeoutException:
        driver.quit()
        check_for_appts()

check_for_appts()