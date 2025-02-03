from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from dotenv import load_dotenv
import os


class BotRaspaTela:
    def __init__(self, links, usuario, senha):
        self.links = links
        self.usuario = usuario
        self.senha = senha

    def browser(self):
        print("ENTREI NO BROWSER")
        for link in self.links:

            driver = webdriver.Chrome()
            driver.get(link)
            time.sleep(0.2)
            driver_user = driver.find_element(By.NAME, "session_key")  # Alterar para o name correto do campo
            driver_pass = driver.find_element(By.NAME, "session_password")

            driver_user.send_keys(str(self.usuario))
            driver_pass.send_keys(str(self.senha))
            driver_pass.send_keys(Keys.RETURN)

            time.sleep(0.2)

            print("COLETANDO INFORMACOES")
            visualizacoes = driver.find_element(By.XPATH, '//li[1]//span/strong').text
            impressoes = driver.find_element(By.XPATH, '//li[2]//span/strong').text

            print("CRIANDO DATAFRAMES")
            df = pd.DataFrame([{
                "Data": pd.Timestamp.today().strftime("%Y-%m-%d"),
                "Visualizações": visualizacoes,
                "impressoes": impressoes}])

            arquivo_excel = "dados_perfil.xlsx"

            print("SALVANDO INFORMACOES")
            try:
                df_existente = pd.read_excel(arquivo_excel)
                df = pd.concat([df_existente, df], ignore_index=True)
            except FileNotFoundError:
                pass  # O arquivo será criado na próxima linha

            df.to_excel(arquivo_excel, index=False)

            print("Dados salvos com sucesso!")
            driver.close()


if __name__ == '__main__':
    user = []
    links = []
    with open('links.txt', 'r') as arquivo:
        for linha in arquivo:
            links.append(linha.replace('\n', ''))

    with open('user.txt', 'r') as arqu_user:
        for linha in arqu_user:
            user.append(linha.replace('\n', ''))

    load_dotenv()
    usuario = os.getenv("email")
    senha = os.getenv("senha")

    info = BotRaspaTela(links, usuario, senha)
    info.browser()
