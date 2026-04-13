# -*- coding: utf-8 -*-

import os
import time
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# =======================
# 1. 设置 Chrome 浏览器
# =======================
def setup_driver(download_dir=None):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # 最大化窗口
    chrome_options.add_argument("--disable-notifications")  # 禁用通知

    if download_dir:
        # 设置默认下载路径
        prefs = {
            "download.default_directory": download_dir,
            "printing.print_preview_sticky_settings.appState": '{"recentDestinations":[{"id":"Save as PDF","origin":"local"}],"selectedDestinationId":"Save as PDF","version":2}',
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument('--kiosk-printing')  # 自动打印 PDF

    service = Service(r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")  # 修改为你的 chromedriver 路径
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# =======================
# 2. 手动登录
# =======================
def login_manual(driver):
    login_url = "https://www.mtslash.life/member.php?mod=logging&action=login"
    driver.get(login_url)
    print("\n" + "="*50)
    print("请在浏览器中完成登录操作。")
    print("登录成功并看到你的收藏或主页后，回到命令行按回车继续。")
    print("="*50 + "\n")
    input("按回车继续...")

# =======================
# 3. 抓取收藏夹链接
# =======================
def scrape_links(driver, total_pages=63):
    base_url = "https://www.mtslash.life/home.php?mod=space&do=favorite&type=all&page={}"
    all_links = []

    for page in range(1, total_pages + 1):
        url = base_url.format(page)
        print(f"正在抓取第 {page} 页...")
        driver.get(url)
        time.sleep(2)  # 等页面加载
        
        try:
            a_tags = driver.find_elements(By.TAG_NAME, "a")
            for a in a_tags:
                href = a.get_attribute("href")
                if href and "thread-" in href:
                    if href not in all_links:
                        all_links.append(href)
        except Exception as e:
            print(f"第 {page} 页抓取出错: {e}")
    
    print(f"\n抓取完成，共 {len(all_links)} 个不重复链接。")
    return all_links

# =======================
# 4. 保存 Excel
# =======================
def save_to_excel(links, filename="favorites.xlsx"):
    df = pd.DataFrame({"links": links})
    df.to_excel(filename, index=False)
    print(f"链接已保存到 Excel 文件: {filename}")

# =======================
# 5. 清理标题中的非法字符
# =======================
def clean_filename(title):
    """将标题转换为合法文件名"""
    title = re.sub(r'[\/:*?"<>|]', '_', title)  # 替换非法字符
    title = title.strip()
    if len(title) > 100:  # 防止太长
        title = title[:100]
    return title

# =======================
# 链接转换函数（提取tid并生成打印链接）
# =======================
def convert_thread_url(original_url):
    match = re.search(r'thread-(\d+)-', original_url)
    if match:
        tid = match.group(1)
        new_url = f"https://www.mtslash.life/forum.php?mod=viewthread&action=printable&tid={tid}"
        return new_url
    return original_url

# =======================
# 6. 保存 PDF（用帖子标题命名）
# =======================
def save_links_as_pdf(driver, links, save_dir="pdfs"):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for idx, link in enumerate(links, start=1):
        try:
            # 转换为打印版链接
            new_link = convert_thread_url(link)
            driver.get(new_link)
            time.sleep(3)  # 等页面加载

            # 获取帖子标题
            try:
                title_element = driver.find_element(By.CSS_SELECTOR, "span.xw1")  # 注意选择器可根据网页调整
                title = title_element.text
            except:
                title = f"post_{idx}"

            filename = clean_filename(title) + ".pdf"
            filepath = os.path.join(save_dir, filename)

            # 打印 PDF
            driver.execute_script('window.print();')  # Chrome + --kiosk-printing 自动保存
            time.sleep(2)
            
            print(f"[{idx}/{len(links)}] 已保存 PDF: {filepath}")
        except Exception as e:
            print(f"[{idx}] 保存 PDF 出错: {link} -> {e}")

# =======================
# 7. 主函数
# =======================
def main():
    print("启动程序...")
    download_dir = os.path.join(os.getcwd(), "pdfs")
    driver = setup_driver(download_dir=download_dir)
    login_manual(driver)

    TOTAL_PAGES = 6  # 修改为你的收藏页总页数
    links = scrape_links(driver, total_pages=TOTAL_PAGES)
    save_to_excel(links)

    save_links_as_pdf(driver, links, save_dir=download_dir)

    driver.quit()
    print("所有任务完成！Excel 和 PDF 已保存。")

# =======================
# 运行入口
# =======================
if __name__ == "__main__":
    main()
