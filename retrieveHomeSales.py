# selenium to run the page
# BS4 to analyze the page for the necessary information
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
# chromeDriver = webdriver.Chrome('C:\\Users\\Alex Trim\\Documents\\GitHub\\hello-world\\AtomPython\\Miscellaneous\\chromedriver.exe')
# chromeDriver = webdriver.Chrome('C:\\Users\\Dean\\Documents\\GitHub\\hello-world\\AtomPython\\Miscellaneous\\chromedriver.exe')
def retrieveDataMain():
    # establish list
    areaList = []
    # initialize the page
    chromeDriver = webdriver.Chrome('C:\\Users\\Alex Trim\\Documents\\GitHub\\hello-world\\AtomPython\\Miscellaneous\\chromedriver.exe')
    # go to the web page
    chromeDriver.get('https://www.cityofmadison.com/assessor/property/salesbyarea.cfm')
    # find the options and get the list
    areaElem = chromeDriver.find_element_by_id('AssessmentArea')
    areaSelect = Select(areaElem)
    areaOptions = areaSelect.options
    for areaOption in areaOptions:
        areaList.append(areaOption.text)
    #grab the first
    areaSelect.select_by_value(areaList[0])
    submitBtn = chromeDriver.find_element_by_css_selector("input[type='submit']")
    submitBtn.click()
    # get data here
    # ......
    # loop over the options
    for areaItem in areaList[1:9]:
        # find the element again
        # areaElem = chromeDriver.find_element_by_id('AssessmentArea')
        # areaSelect = Select(areaElem)
        # areaSelect.select_by_value(areaItem)
        # find the element a new way
        areaInput = chromeDriver.find_element_by_id('AssessmentArea')
        chromeDriver.execute_script("arguments[0].value = " + areaItem + ";",areaInput)
        # find submit and click it
        submitBtn = chromeDriver.find_element_by_css_selector("input[type='submit']")
        submitBtn.click()
        # area page data loads
        # do something
        # nav back to main page
        # chromeDriver.back()
    # close browser
    chromeDriver.close()


if __name__ == '__main__':
    retrieveDataMain()
# loop over the possible area values, use date sort
# submit to get the home sales data
