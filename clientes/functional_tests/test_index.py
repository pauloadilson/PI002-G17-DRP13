# "C:\Users\paulo\OneDrive\_UNIVESP\programas\rewards\msedgedriver.exe"
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from django.urls import reverse

class TestIndex(StaticLiveServerTestCase):
    def setUp(self):
        # Instancie um objeto EdgeOption
        self.edge_options = webdriver.EdgeOptions()

        # Defina o modo sem cabeçalho
        self.edge_options.headless = True
        
        # Inicie o driver, passando edge_options
        self.driver = webdriver.Edge(options=self.edge_options)

        self.index_url = self.live_server_url + reverse('index')

    def tearDown(self):
        self.driver.quit()
    
    
    def test_index(self):
        # testar se a página inicial está funcionando
        self.page = self.driver.get(self.live_server_url)

        # verificar se a url está correta
        self.assertEqual(self.driver.current_url, self.index_url)

        # verificar se o título da página está correto
        titulo_pagina = self.driver.title
        self.assertEqual(titulo_pagina, "Página inicial")
        
        # verificar se a saudação está correta
        element = self.driver.find_element(By.XPATH,"/html/body/div/main/div/div/div[1]")
        self.assertEqual(element.text, "Bem Vindo(a)")

        # verificar se o texto da página está correto
        element = self.driver.find_element(By.XPATH,"/html/body/div/main/div/div/div[2]/h3")
        self.assertEqual(element.text, "Este é um site desenvolvido como atividade avaliativa para o Projeto Integrador em Computação II")
