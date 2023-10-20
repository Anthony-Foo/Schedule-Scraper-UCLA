from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome()
classDict = {}
url = ("https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Computer+Science+("
       "COM+SCI)&t=23F&sBy=subject&subj=COM+SCI&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex")
def pullData(urlFunc, pageNum):
    driver.get(urlFunc)
    driver.maximize_window()
    driver.implicitly_wait(20)

    # Enter the shadow root and expand all classes on the page
    shadow_content = driver.find_element(By.XPATH, value="/html/body/main/div/div/div["
                                                         "2]/div/div/div/div/div/ucla-sa-soc-app").shadow_root
    if pageNum != 1:
        pageNumStr = str(pageNum)
        (shadow_content.find_element(By.CSS_SELECTOR, '#divPagination > div:nth-child(2) > ul > li:nth-child(' + pageNumStr + ') > button')
    .click())
    sleep(3)
    shadow_content.find_element(By.ID, "expandAll").click()
    driver.implicitly_wait(20)
    sleep(3)

    # find all the html elements under relevant class names and assign it to list
    time_text = shadow_content.find_elements(By.CLASS_NAME, "timeColumn")
    day_text = shadow_content.find_elements(By.CLASS_NAME, "dayColumn")
    section_text = shadow_content.find_elements(By.CLASS_NAME, "sectionColumn")
    class_text = shadow_content.find_elements(By.CLASS_NAME, "linkLikeButton")

    # Slaps webelements into lists of text (i know it can be a function but its like 2 lines so fuck it)
    timeList = []
    lectureList = []
    classList = []
    dayList = []
    for i in day_text:
        dayList.append(i.text)
    for i in time_text:
        timeList.append(i.text)
    for i in section_text:
        lectureList.append(i.text)
    for i in class_text:
        classList.append(i.text)

    # Remove excess data from classList, leaving only the class titles
    classInd = 0
    while classInd < len(classList):
        if " - " not in classList[classInd] or "Online - Asynchronous" in classList[classInd]:
            del classList[classInd]
        else:
            classInd += 1

    # y e s
    print("Lecture and discussions list length:", len(lectureList))
    print("Class dates list length:", len(dayList))
    print("Class times list length:", len(timeList))
    print("\n--------------------------\n")

    # Combine the lecture/discussion, date, and time together in each index
    pairedLectureList = []
    if len(timeList) == len(lectureList) and len(timeList) == len(dayList):
        for i in range(len(timeList)):
            pairedLectureList.append(lectureList[i] + " ; " + dayList[i] + " ; " + timeList[i])

    # Find all the separations between different class lecture times, and create list of their indexes
    lectureIndex = []
    for i in range(len(pairedLectureList)):
        if 'Section' in pairedLectureList[i] or 'Sect' in pairedLectureList[i]:
            lectureIndex.append(i)
    lectureIndex.append(len(pairedLectureList))

    # Assign lectures to their respective classes, while also moving each lecture and its discussions into nested lists
    for index, element in enumerate(classList):
        tempLecList = []
        discussInd = []
        tempNest = []
        for i in range(lectureIndex[index] + 1, lectureIndex[index + 1]):
            tempLecList.append(pairedLectureList[i])
        for location, entry in enumerate(tempLecList):
            if "Lec" in entry or "Sem" in entry or "Lab" in entry or "Tut" in entry:
                discussInd.append(location)
        discussInd.append(len(tempLecList))
        for i in range(len(discussInd) - 1):
            tempNest.append(tempLecList[discussInd[i]:discussInd[i + 1]])
        classDict[element] = tempNest
    return classDict

print(pullData(url, 1))
print(pullData(url, 2))
