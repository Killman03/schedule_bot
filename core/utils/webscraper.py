from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from core.utils.pro_auth import *
import zipfile
import csv
from aiogram import Bot
from aiogram.types import Message

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


class BotWindow():
    def __init__(self, use_proxy=False, user_agent=None):
        chrome_options = webdriver.ChromeOptions()
        if user_agent:
            chrome_options.add_argument(f'user-agent={user_agent}')
        if use_proxy:
            pluginfile = 'proxy_auth_plugin.zip'
            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
            chrome_options.add_extension(pluginfile)

        chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(
            options=chrome_options,
        )

    def csv_writing(self, info_lines):
        self.info_lines = info_lines

        header = ['data', 'time', 'lesson']

        with open("ajk.csv", "a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(self.info_lines)

    def get_driver(self):
        try:
            self.driver.get('https://vgltu.ru/obuchayushchimsya/raspisanie-zanyatij/')
            src_group = self.driver.find_element(By.ID, 'searchGroup')
            src_group.clear()
            src_group.send_keys('МиР2-221-ОБ')
            src_group.send_keys(Keys.ENTER)
            time.sleep(1)
            # Values for text
            main = self.driver.find_element(By.ID, 'raspTableGroup')
            table = main.find_elements(By.TAG_NAME, 'tbody')

            raspis = ''

            for i in table:
                k = i.find_elements(By.TAG_NAME, 'tr')
                for j in k:
                    raspis += j.text
                    raspis += '\n\n'
                break
            return raspis

        except Exception as e:
            print(e)
            self.driver.close()


def read_csv_file():
    with open('ajk.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)


def send_lessons():
    bot = BotWindow(use_proxy=False)
    res = bot.get_driver()
    time.sleep(1)
    bot.driver.close()
    return res


if __name__ == '__main__':
    print(send_lessons())
