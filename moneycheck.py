__author__ = 'jensaronsson'

import requests
from bs4 import BeautifulSoup


class Banking:

    baseUrl = "https://mobilbank.swedbank.se/banking/swedbank/"

    def __init__(self):
        self.pn = raw_input("personal number")
        self.pw = raw_input("password")
        self.req = requests.Session()


    def get_csrf_token(self, content):
        content = BeautifulSoup(content)
        return content.form.div.div.input['value']

    def get_url(self, action):
        return self.baseUrl + action + ".html"

    def login(self):
       response = self.req.get(self.get_url("login"))
       payload = {'auth-method': 'code', 'xyz': self.pn, '_csrf_token':self.get_csrf_token(response.content), 'busJavascriptSupported': 'true'}


       response = self.req.post(self.get_url("loginNext"), data = payload)

       payload = {'zyx': self.pw, '_csrf_token': self.get_csrf_token(response.content)}
       self.req.post(self.get_url("login"), data = payload)

    def get_accounts(self):
        response = self.req.get(self.get_url('accounts'))
        dom = BeautifulSoup(response.text)
        for account in dom.dl.find_all('dd'):
            print account.find('span', 'name').string.strip() + " : " + account.find('span', 'amount').string.strip() + " kr"

b = Banking()
b.login()
b.get_accounts()

