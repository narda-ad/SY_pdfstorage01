#貌似下载有点小问题，懒得改了哈哈哈
# coding=utf-8
import pandas as pd
import time
import openpyxl
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def scrape_links_from_excel(file_path):
    """从 Excel 文件中读取超链接"""
    main_book = openpyxl.load_workbook(file_path)
    main_sheet = main_book.active
    links = []
    for row in main_sheet.iter_rows(min_row=2, min_col=1, max_col=1):
        cell = row[0]
        if cell.hyperlink:
            url = cell.hyperlink.target
            links.append(url)
        elif cell.value:
            print(f"单元格包含值: {cell.value}（但不是超链接）")
    return links

def setup_webdriver():
    """设置 Selenium webdriver"""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": os.getcwd(),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    service = Service('C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def click_and_scrape(driver, url):
    """点击链接并执行打印保存操作"""
    driver.get(url)
    time.sleep(5) 

    try:
        print(f"正在尝试处理: {url}")
        print_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[title='打印']"))
        )
        print_link.click()
        time.sleep(3)

        pyautogui.hotkey('ctrl', 'p')
        time.sleep(4)

        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        
        return url, "执行完毕"

    except Exception as e:
        print(f"在 {url} 处理时发生错误: {e}")
        return None, None

def main():
    input_file = 'mtslash_favorites_selenium.xlsx'

    try:
        links = scrape_links_from_excel(input_file)
    except Exception as e:
        print(f"读取文件失败: {e}")
        return

    if not links:
        print("未找到链接。")
        return

    driver = setup_webdriver()

    print("正在打开登录页面...")
    driver.get("https://www.mtslash.life/member.php?mod=logging&action=login")

    print("\n" + "="*50)
    print("【人工干预步骤】：")
    print("1. 请在弹出的浏览器中完成登录。")
    print("2. 确保页面已经成功登录并能看到你的收藏或主页。")
    print("3. 回到这个命令行窗口，按下 [回车键] 开始自动下载。")
    print("="*50 + "\n")
    
    input("登录完成后，请按回车键继续...")

    for link in links:
        print(f"当前处理: {link}")
        res_url, status = click_and_scrape(driver, link)
        if res_url:
            print(f"成功: {status}")
        else:
            print(f"失败: {link}")
        
        time.sleep(2)

    print("所有任务处理完成。")
    driver.quit()

if __name__ == '__main__':
    main()
