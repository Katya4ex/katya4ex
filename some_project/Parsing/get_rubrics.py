
import csv
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def write_csv(data):
    with open('rubrics.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['name_rubric'],
                         data['name_subrubric'],
                         data['url_rubric'],
                         data['url_subrubric'],
                         ))


def get_page(url):
    driver = webdriver.Chrome()
    driver.implicitly_wait(1)
    driver.get(url)
    return driver


def main():
    url = 'https://2gis.ru/spb/rubrics'
    driver = get_page(url)
    count_rubrics = len(driver.find_elements_by_class_name('_mq2eit'))

    try:
        for ur in range(count_rubrics):
            rubric = driver.find_elements_by_class_name('_dawz3y')
            url_rubric = rubric[ur].get_attribute('href')
            correct_url = re.search(r'rubrics', url_rubric)
            if correct_url is None:
                continue
            name_rubric = rubric[ur].get_attribute('title')
            rubric[ur].click()

            WebDriverWait(driver, 3).until(
                    EC.text_to_be_present_in_element((By.CLASS_NAME,
                                                      '_o6zo96'), name_rubric)
                )
            count_subrub = len(driver.find_elements_by_class_name('_mq2eit'))
            for url in range(count_rubrics, count_subrub):
                subrubric = driver.find_elements_by_class_name('_dawz3y')
                url_subrubric = subrubric[url].get_attribute('href')
                name_subrubric = subrubric[url].get_attribute('title')

                data = {'name_rubric': name_rubric,
                        'url_rubric': url_rubric,
                        'name_subrubric': name_subrubric,
                        'url_subrubric': url_subrubric}
                write_csv(data)

    finally:
        driver.quit()


if __name__ == '__main__':
    main()
