# SY_pdf_storage
自动化下载随缘收藏夹的文章成pdf格式的，没事时可以闲来下载了看看文~

# 随缘居收藏夹批量导出（Excel + PDF）
一键登录随缘居 → 抓取收藏帖子链接 → 导出Excel → 自动保存为PDF（按帖子标题命名）

## 😃目前支持电脑上有chrome和python的
## 😊直接使用“Easy_Way.py”这个文件就可以了，另外两个是分体的方便找错error不过我感觉只要Easy_Way.py也没啥报错了hh，右上角下载这个代码，在你的命令框运行即可

---
## 一、使用步骤
1. **安装依赖**
先确保你的电脑安装了python，然后进行pip安装（就是复制这个到cmd）
```bash
pip install pandas selenium openpyxl
```

2. **配置 ChromeDriver**
- 下载与你的Chrome版本匹配的`chromedriver.exe`
- 将代码中路径改为你本地的真实路径：（例）
```python
service = Service(r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")
```

3. **修改收藏页数**
在`main()`中修改为你自己的！！！收藏总页数！！：（要是有一百页就写100，要是20也就写20）
```python
TOTAL_PAGES = 6
```

4. **运行脚本**
- 弹出浏览器后**手动登录**
- 登录成功回到命令行（就是那个黑黑框任意位置）按回车
- 程序自动抓取链接 → 保存Excel → 批量保存PDF

---

## 二、输出文件
- `favorites.xlsx`：所有收藏帖子链接
- `pdfs/`文件夹：所有帖子PDF（标题命名）

---

## 三、注意事项
- 运行期间**不要关闭浏览器**
- 不要操作鼠标键盘，避免干扰自动化
- 网页加载慢可适当调大`time.sleep()`数值（个别帖子太长的加载很慢或者你网络不好都会少爬取几个，不过可以再试试看）
- PDF默认保存到电脑下载界面
---

### 极简说明 先登录 → 自动抓收藏 → 自动存Excel → 自动导出PDF


- ### 另：话说这个可以适配edge吗？
- 可以的，基本思路和 Chrome 一模一样，因为 Edge 内核就是 Chromium，Selenium 对 Edge 的支持和 Chrome 非常相似。
- 但是要做以下改动：
- 1️⃣ 安装 Edge WebDriver
- 下载 Edge 对应版本的驱动：Microsoft Edge WebDriver
- 解压放在某个文件夹（比如 C:\WebDriver\msedgedriver.exe）
- 2️⃣ 修改代码：使用 Edge 而不是 Chrome
- 把原来的 setup_driver() 改掉（嗯呐可以问问ai）
- 然后在主函数中：- driver = setup_driver_edge()
- 有需求的可以试试看~

- 嗯嗯其实感觉是有更快地方式比如保存html再转pdf什么的，但是感觉会有很多不相关的页面元素，而且还要做页面内的翻页问题，所以还是用随缘自己的print打印清爽一点，自己看问的时候也方便哈哈。
- 欢迎提issue，fork，或者你要是给我小星星star我也会很感激的哈哈^_^
