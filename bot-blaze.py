from datetime import date
import glob
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from collections import Counter
import datetime
import pytz

# RED = 1
# BLACK = 2
# WHITE = 3

def getLastResults():
    driver = webdriver.Chrome()
    folderPath = "C:\\source\\BotDouble"

    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : folderPath}
    chromeOptions.add_experimental_option("prefs",prefs)
    chromedriver = "./chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chromedriver, options=chromeOptions)
    
    driver.get('https://tipminer.com/resultados/blaze/double')
    driver.maximize_window()
    time.sleep(2)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/header/div/div/button")))
    accessButton = driver.find_element(By.XPATH, "/html/body/div[2]/header/div/nav/button")
    accessButton.click()
    time.sleep(4)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/main/div/div/form/div/div[2]/div[2]/div/button")))

    login = 'guilherme.msantanaa@gmail.com'
    password = 'Gui34785535'
    loginField = driver.find_element(By.XPATH, "//*[@id='email']")
    loginField.send_keys(login)
    passField = driver.find_element(By.XPATH, "//*[@id='password']")
    passField.send_keys(password)
    loginButton = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/main/div/div/form/div/div[2]/div[2]/div/button")
    loginButton.click()
    time.sleep(2)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/main/div/div[2]/div[2]/form/div/div[1]/div/div/button[1]")))
    excelButton = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/main/div/div[2]/div[2]/form/div/div[1]/div/div/button[1]")
    excelButton.click()
    time.sleep(10)

    while not any(file.endswith(".xlsx") for file in os.listdir(folderPath)):
        time.sleep(1)

    driver.quit()

    df = pd.read_excel('./tipminer-dados.xlsx')

    for file in glob.glob(folderPath + "/*.xlsx"):
            if os.path.isfile(file) and file.endswith(".xlsx"):
                os.remove(file)
    
    lastResultsExcel = df["Cor"].values.tolist()
    lastResultsNumber = []
    for result in lastResultsExcel:
        if result == 'vermelho':
            lastResultsNumber.append(1)
        elif result == 'preto':
            lastResultsNumber.append(2)
        elif result == 'branco':
            lastResultsNumber.append(3)

    return lastResultsNumber


def startOperation(triggerSequence):
    driver = webdriver.Chrome()
    driver.get('https://blaze.com/pt/games/double')
    time.sleep(6)
    triggerHistory = []

    while True:
        lastValues = []

        recentResults = driver.find_element(By.XPATH, "//*[@id='roulette-recent']/div/div[1]")
        rouletteValues = recentResults.find_elements(By.CLASS_NAME, "roulette-tile")
            
        for v in rouletteValues:
            result = v.find_element(By.XPATH, './div')
            className = result.get_attribute('class')
            if className != None:
                if 'red' in className:
                    lastValues.append(1)
                    triggerHistory.append(Values(1, 'false'))
                elif 'black' in className:
                    lastValues.append(2)
                    triggerHistory.append(Values(2, 'false'))
                else:
                    lastValues.append(3)
                    triggerHistory.append(Values(3, 'false'))
        
        print(f'Resultado atual: {lastValues[0]}')

        if triggerHistory[1].isTrigger == 'true':
            if triggerHistory[0].number == triggerHistory[0].expectedValue:
                saveResult('Gain')
            else:
                saveResult('Loss')
            triggerHistory = []

        if lastValues[0] == triggerSequence[2] and lastValues[1] == triggerSequence[1] and lastValues[2] == triggerSequence[0]:
            fuso_horario_sp = pytz.timezone('America/Sao_Paulo')
            data_hora_sp = datetime.datetime.now(fuso_horario_sp)
            data_hora_formatada = data_hora_sp.strftime('%d/%m/%Y %H:%M:%S')
            triggerHistory[0].isTrigger = 'true'
            triggerHistory[0].expectedValue = lastValues[0]      
            saveResult(f'Entrou ás: {data_hora_formatada}, Em uma vela {lastValues[0]}, Experando uma vela: { triggerSequence[3]}') 

        time.sleep(3)

    driver.quit()

def getTriggerSequence(lastResultsList):
    count = Counter(zip(lastResultsList, lastResultsList[1:], lastResultsList[2:], lastResultsList[3:]))
    mostCommomReps = count.most_common()
    return mostCommomReps[0][0]
    #print("The sequence of 4 most repeated numbers is:", mostCommomReps[0][0], "with", mostCommomReps[0][1], "occurrences.")

def saveResult(message):
    arquivo = open("blaze-results.txt", "a")
    arquivo.write(message)
    arquivo.close()

class Values:
    def __init__(self, number, isTrigger, expectedValue=None):
        self.number = number
        self.isTrigger = isTrigger
        self.expectedValue = expectedValue

lastResultsList = getLastResults()
print('lastResultsList: ', lastResultsList)
triggerSequence = getTriggerSequence(lastResultsList)
print('triggerSequence: ', triggerSequence)
startOperation(triggerSequence)




