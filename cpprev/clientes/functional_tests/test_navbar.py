# "C:\Users\paulo\OneDrive\_UNIVESP\programas\rewards\msedgedriver.exe"
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from django.urls import reverse

class TestNavBar(StaticLiveServerTestCase):
    def setUp(self):
        # Instancie um objeto EdgeOption
        self.edge_options = webdriver.EdgeOptions()

        # Defina o modo sem cabeçalho
        self.edge_options.headless = True
        
        # Inicie o driver, passando edge_options
        self.driver = webdriver.Edge(options=self.edge_options)
        

    def tearDown(self):
        self.driver.quit()
    
    def test_navbar(self):
        # Obtenha a página
        self.page = self.driver.get(self.live_server_url)
        
        # Encontre o link para a página de clientes e clique nele
        element = self.driver.find_element(By.XPATH,"/html/body/nav/div/div/ul/li[3]/a")
        self.assertEqual(element.text, "Clientes")
        element.click()
        clientes_url = self.live_server_url + reverse('clientes')
        self.assertEqual(self.driver.current_url, clientes_url)
        
        # Encontre o link para a página de início e clique nele
        element = self.driver.find_element(By.XPATH,"/html/body/nav/div/div/ul/li[1]/a")
        self.assertEqual(element.text, "Início")
        element.click()
        index_url = self.live_server_url + reverse('index')
        self.assertEqual(self.driver.current_url, index_url)
        
