import selenium
from selenium import webdriver
import re
from datetime import datetime
import getpass


def get_paedagogik_end_date(browser, url, xpath):
    browser.get(url)
    text = browser.find_element_by_xpath(xpath)
    search_date = text.text  # convert in text to filter Dates
    find_phase_text = search_date.find("1. Phase")
    dates_plus_text = search_date[find_phase_text:315]

    match = re.findall(r'\d{2}.\d{2}.\d{4}', dates_plus_text)

    end_date = datetime.strptime(match[1], "%d.%m.%Y")
    return end_date


def get_end_date(browser, url, xpath):
    browser.get(url)
    text = browser.find_element_by_xpath(xpath)
    search_date = text.text  # convert in text to filter Dates
    find_phase_text = search_date.find("Anmelde")
    dates_plus_text = search_date[find_phase_text:200]

    match_yyyy = re.findall(r'\d{2}.\d{2}.\d{4}', dates_plus_text)
    match_yy = re.findall(r'\d{2}.\d{2}.\d{2}', dates_plus_text)

    if match_yyyy:
        end_date = datetime.strptime(match_yyyy[1], "%d.%m.%Y")
    else:  # convert yy format in yyyy for later comperison
        end_date = datetime.strptime(match_yy[1], "%d.%m.%y").strftime("%d.%m.%Y")
        end_date = datetime.strptime(end_date, "%d.%m.%Y")
    return end_date


def days_till_deadline(today_in, end_date):
    days_till_end_date = end_date - today_in
    end_date_as_string = end_date.strftime("%d.%m.%Y")
    if days_till_end_date.days < 0:

        print("\nDas Anmeldedatum ist bereits vorbei.")
        print("Die Deadline war am " + end_date_as_string)
    else:
        print("\nEs sind noch " + str(days_till_end_date.days) + " Tage bis zum Ende der Anmeldefrist ("
             + end_date_as_string + ")")


if __name__ == "__main__":
    user = str(getpass.getuser())
    driver_path = "C:\\Users\\" + user + r"\OneDrive\Dokumente\Python\Anmeldefristen\chromedriver.exe"
    driver = webdriver.Chrome(driver_path)
    url_paedagogik = "https://ufind.univie.ac.at/de/vvz_sub.html?semester=2021S&path=258956"
    url_info = "https://informatik.univie.ac.at/studium/hilfe-fuer-studierende/anmeldung-zu-lehrveranstaltungen-pruefungen/#c1597"
    url_physik = "https://ssc-physik.univie.ac.at/#:~:text=Dazu%20m%C3%BCssen%20Sie%20sich%20bis,Tage%20vor%20dem%20Pr%C3%BCfungstermin%20erfolgen."
    xpath_paedagogik = "/html/body/main/div[3]/div[1]"  # path sometimes doesn't work (don't know why)
    xpath_info = '//*[@id="c1597"]/div/div/div[1]/div/div/ul/li[1]/ul'
    xpath_physik = '//*[@id="c687853"]/div/div/div[1]/div/ol/li[2]'

    today = datetime.today()
    xpath_found = False
    count = 1
    while not xpath_found and count != 10:  # loop for trying multiple times, till xpath works, or tried 10 times
        try:
            paedagogik_end_date = get_paedagogik_end_date(driver, url_paedagogik, xpath_paedagogik)
            days_till_deadline(today, paedagogik_end_date)
            xpath_found = True
            count = 10
        except selenium.common.exceptions.NoSuchElementException as err:
            xpath_found = False
        count += 1
    try:
        info_end_date = get_end_date(driver, url_info, xpath_info)
        days_till_deadline(today, info_end_date)
    except selenium.common.exceptions.NoSuchElementException as err:
        print("XPath konnte nicht richtig durchsucht werden.".format(err))
    try:
        physik_end_date = get_end_date(driver, url_physik, xpath_physik)
        days_till_deadline(today, physik_end_date)
    except selenium.common.exceptions.NoSuchElementException as err:
        print("XPath konnte nicht richtig durchsucht werden.".format(err))

    current_date = today.strftime("%d.%m.%Y")
    print("\nHeute ist der: " + current_date)

    driver.close()
