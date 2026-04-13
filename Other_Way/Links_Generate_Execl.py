#pip install pandas selenium openpyxl #如果没装的话
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def main():
    chrome_options = Options()
    service = Service('C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe') 
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print("正在打开浏览器...")
    driver.get("https://www.mtslash.life/member.php?mod=logging&action=login")

    input("\n【重要操作】请在弹出的浏览器窗口中手动完成登录。\n登录成功后按下回车键继续...")

    TOTAL_PAGES = 6
    base_url = "https://www.mtslash.life/home.php?mod=space&do=favorite&type=all&page={}"
    
    extracted_links = []

    for page in range(1, TOTAL_PAGES + 1):
        print(f"正在抓取第 {page} 页...")
        url = base_url.format(page)
        
        driver.get(url)
        time.sleep(2)
        
        try:
            a_tags = driver.find_elements(By.TAG_NAME, "a")
            
            for a in a_tags:
                href = a.get_attribute('href')
                
                if href and 'thread-' in href:
                    if href not in [item['links'] for item in extracted_links]:
                        extracted_links.append({'links': href})
                        
        except Exception as e:
            print(f"抓取第 {page} 页时发生小错误: {e}")

    print(f"\n抓取完成，共提取到 {len(extracted_links)} 个不重复的链接。正在写入 Excel...")
    driver.quit()
    
    df = pd.DataFrame(extracted_links)
    excel_filename = "mtslash_favorites_selenium.xlsx"
    df.to_excel(excel_filename, index=False)
    print(f"保存成功！文件已生成为：{excel_filename}")

if __name__ == "__main__":
    main()
