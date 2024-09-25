# "C:\Users\paulo\OneDrive\_UNIVESP\programas\rewards\msedgedriver.exe"
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from django.urls import reverse

class TestClientes(StaticLiveServerTestCase):
    def setUp(self):
        # Instancie um objeto EdgeOption
        self.edge_options = webdriver.EdgeOptions()

        # Defina o modo sem cabeçalho
        self.edge_options.headless = True
        
        # Inicie o driver, passando edge_options
        self.driver = webdriver.Edge(options=self.edge_options)

        self.novo_cliente_url = self.live_server_url + reverse('novo_cliente')
        self.clientes_url = self.live_server_url + reverse('clientes')

        self.cliente1 = {
            "cpf": "12345678901",
            "nome": "Fulano de Tal",
            "data_nascimento": "21/01/1981",
            "telefone_whatsapp": "18991234567",
            "email": "paulo@paulo.com",
        }

    def tearDown(self):
        self.driver.quit()
    
    
    def test_clientes_page(self):
        # testar se a página de clientes está funcionando

        # incluindo um cliente
        self.client.post(self.novo_cliente_url, {
            "cpf": "12345678901",
            "nome": "Fulano de Tal",
            "data_nascimento": "1981-01-21",
            "telefone_whatsapp": "18991234567",
            "email": "paulo@paulo.com",
        })

        # testar se a página de clientes está funcionando
        self.page = self.driver.get(self.clientes_url)
        element = self.driver.find_element(By.XPATH,"/html/body/div/main/div/div[1]/div")
        self.assertEqual(element.text, "Clientes")
        
        # verificar se o botão editar está presente
        element = self.driver.find_element(By.XPATH,"/html/body/div/main/div/div[2]/table/tbody/tr/td[7]/a[1]")
        name_attribute = element.get_attribute("atitle")
        self.assertEqual(name_attribute, "Editar")

        # verificar se o botão excluir está presente
        element = self.driver.find_element(By.XPATH,"/html/body/div/main/div/div[2]/table/tbody/tr/td[7]/a[2]")
        name_attribute = element.get_attribute("atitle")
        self.assertEqual(name_attribute, "Excluir")

        # verificar se o botão novo cliente está presente e funcionando
        element = self.driver.find_element(By.XPATH,"/html/body/div/main/div/div[1]/p/a")
        self.assertEqual(element.text, "Novo Cliente")
        element.click()
        self.assertEqual(self.driver.current_url, self.novo_cliente_url)



    def test_novo_cliente_page(self):
        # testar se a página de novo cliente está funcionando
        self.page = self.driver.get(self.clientes_url)
        element = self.driver.find_element(By.XPATH,"/html/body/div/main/div/div[1]/p/a")
        element.click()

        element = self.driver.find_element(By.XPATH,"/html/body/div[1]/main/div/div[1]/div")
        self.assertEqual(element.text, "Novo Cliente")
        
        # verificar se o botão salvar está presente
        element = self.driver.find_element(By.XPATH,"/html/body/div[1]/main/div/div[2]/form/div[7]/div/input[1]")
        name_attribute = element.get_attribute("value")
        self.assertEqual(name_attribute, "Salvar")
        
        # verificar se o botão voltar está presente e funcionando
        element = self.driver.find_element(By.XPATH,"/html/body/div[1]/main/div/div[2]/form/div[7]/div/input[2]")
        name_attribute = element.get_attribute("value")
        self.assertEqual(name_attribute, "Voltar")
        element.click()
        self.assertEqual(self.driver.current_url, self.clientes_url)

        
    def test_novo_cliente_insert_and_check(self):
        # verificar se o formulário está funcionando
        self.page = self.driver.get(self.novo_cliente_url)
        self.driver.maximize_window()

        element = self.driver.find_element(By.XPATH,"/html/body/div[1]/main/div/div[2]/form/div[1]/input")
        element.send_keys(self.cliente1['cpf'])
        element = self.driver.find_element(By.XPATH,"/html/body/div[1]/main/div/div[2]/form/div[2]/input")
        element.send_keys(self.cliente1['nome'])
        element = self.driver.find_element(By.XPATH,"/html/body/div[1]/main/div/div[2]/form/div[3]/input")
        element.send_keys(self.cliente1['data_nascimento'])
        element = self.driver.find_element(By.XPATH,"/html/body/div[1]/main/div/div[2]/form/div[4]/input")
        element.send_keys(self.cliente1['telefone_whatsapp'])
        element = self.driver.find_element(By.XPATH,"/html/body/div[1]/main/div/div[2]/form/div[6]/input")
        element.send_keys(self.cliente1['email'])
        element = self.driver.find_element(By.XPATH,"/html/body/div[1]/main/div/div[2]/form/div[7]/div/input[1]")
        element.click()
        self.assertEqual(self.driver.current_url, self.clientes_url)
        time.sleep(5)
        print('Esperando 5 segundos para verificar se o cliente foi salvo')
        element = self.driver.find_element(By.XPATH,"/html/body/div/main/div/div[1]/div")
        self.assertEqual(element.text, "Clientes")

        # verificar se o cliente foi salvo
        element = self.driver.find_element(By.XPATH,"/html/body/div/main/div/div[2]/table/tbody/tr/td[1]")

        self.assertEqual(element.text, self.cliente1['cpf'])
        element = self.driver.find_element(By.XPATH,"/html/body/div/main/div/div[2]/table/tbody/tr/td[2]")
        self.assertEqual(element.text, self.cliente1['nome'])
        element = self.driver.find_element(By.XPATH,"/html/body/div/main/div/div[2]/table/tbody/tr/td[3]")
        self.assertEqual(element.text, self.cliente1['data_nascimento'])
        element = self.driver.find_element(By.XPATH,"/html/body/div/main/div/div[2]/table/tbody/tr/td[4]")
        self.assertEqual(element.text, self.cliente1['telefone_whatsapp'])
        element = self.driver.find_element(By.XPATH,"/html/body/div/main/div/div[2]/table/tbody/tr/td[5]")
        self.assertEqual(element.text, "None")
        element = self.driver.find_element(By.XPATH,"/html/body/div/main/div/div[2]/table/tbody/tr/td[6]")
        self.assertEqual(element.text, self.cliente1['email'])
