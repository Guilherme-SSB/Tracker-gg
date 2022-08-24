import json
import os

import requests
import undetected_chromedriver as uc
from colorama import Fore, Style, init
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Config Colorama - Usado para colorir o texto no terminal
init(convert=True)
red = Fore.RED
green = Fore.GREEN
yellow = Fore.YELLOW
reset = Style.RESET_ALL

def clean_screen():
    """
    Limpa o terminal.
    """
    os.system('cls || clear')


def iniciate_chromedriver(undetected_chromedriver=False) -> webdriver:
    """
    Cria uma instancia do webdriver do Chrome, em uma guia anônima.
    É possível usar o webdriver sem a necessidade de instalar o ChromeDriver, visto que estamos passando
    um Service para a função, que é responsável por iniciar o ChromeDriver na versão mais recente.
    
    Se undetected_chromedriver=True, instancia um webdriver "mais anônimo" (Pode ser útil em alguns
    casos em que o site está bloqueando a coleta).


    Parâmetros
    ----------
    undetected_chromedriver: Se desejar usar o webdriver "mais anônimo", basta passar True.
    Por default é False
    
    Retorna
    -------
    Objeto webdriver do Chrome.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")
    
    if undetected_chromedriver:
        driver = uc.Chrome(options=options)
        driver.maximize_window()
        os.system('cls || clear')
        return driver
        
    else:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.maximize_window()
        os.system('cls || clear')
        return driver


def find_element_by_xpath(driver: webdriver, xpath: str):
    """
    Busca um elemento pelo xpath, com uma tolerância de 5 segundos.
    
    Parâmetros
    ----------
    driver: objeto webdriver do Chrome.
    xpath: string com o xpath do elemento.
    
    Retorna
    -------
    O elemento que foi encontrado.
    """
    return WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))


def find_elements_by_class_name(driver: webdriver, class_name: str):
    """
    Busca um elemento pelo class_name, com uma tolerância de 5 segundos.
    
    Parâmetros
    ----------
    driver: objeto webdriver do Chrome.
    class_name: string com o class_name do elemento.
    
    Retorna
    -------
    O elemento que foi encontrado.
    """
    return driver.find_elements(By.CLASS_NAME, class_name)


def check_exists_by_xpath(driver, xpath) -> bool:
    """
    Se o elemento buscado existir, retorna True, caso contrário, retorna False.
    
    Parâmetros
    ----------
    driver: objeto webdriver do Chrome.
    xpath: string com o xpath do elemento.

    Retorna
    -------
    True se o elemento existir, False caso contrário.
    """
    try:
        find_element_by_xpath(driver, xpath)
    except TimeoutException:
        return False
    return True
