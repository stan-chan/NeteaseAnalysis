### 需求说明

通过浏览器自动化测试工具selenium爬取网易云歌曲下的评论，并对评论生成词云进行分析。

### 环境部署

1. 安装selenium

```shell
pip install selenium
```

2. 安装浏览器driver

```
1. Chrome
//查看chrome浏览器版本
chrome://version
//下载对应版本的chromedriver
https://npm.taobao.org/mirrors/chromedriver/
//将chromedriver拷贝到usr/local/bin
//若出现MacOS无法打开“chromedriver”
cd usr/local/bin
xattr -d com.apple.quarantine chromedriver
或者
spctl --add --label'Approved'< of-executable>

2. Microsoft Edge
//查看edge浏览器版本
edge://version
//下载地址
https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

3.Safari
//打开开发者模式
//允许远程自动化
```

### 爬取数据

爬取歌曲评论，将评论写入comments.txt

```python
from selenium import webdriver
# dirver连续使用几次后会爬取卡顿，待优化
# 暂时可以通过切换浏览器driver继续使用
# driver = webdriver.Safari()
# driver = webdriver.Chrome()
driver = webdriver.Edge()
driver.get(url)
driver.switch_to.frame(0)

for click in range(10):
  divs = driver.find_element_by_css_selector('.cnt.f-brk').text
  cnt = cnt.replace('\n', ' ')
  cnt = re.findall(': (.*)', cnt)[0]
  print(cnt)
  with open('comments.txt', mode='a', encoding='utf-8') as f:
    f.write(cnt + '\n')
  
  dirver.find_element_by_css_selector('.znxt').click()
  time.sleep(0.5)
 
driver.quit()
```

### 数据处理

读取生成的评论文件，数据格式处理

```python
import jieba
file = open('comments.txt', encoding='utf-8')
txt = file.read()
# 分词
txt_list = jieba.lcut(txt)
txt_str = " ".join(txt_list)
```

### 生成词云

```python
img = Image.open("sharp.png")
wc = worldcloud.WordCloud(
collocations=False,
# 尺寸过大会导致自动打开失败
width=500,
height=400,
background_color="white",
# 选择本机已安装的字体文件，文件错误会导致词云显示中文异常
font_path='/Library/Fonts/Arial Unicode.ttf'
scale=15,
# 过滤词
stopwords=set([line.strip() for line in open('stopwords.txt', mode='r').readlines()])
)
wc.generate(txt_str)
wc.to_file("wordcloud.png")
```

### 词云显示

```python
image = Image.open('wordcloud.png')
plt.figure('wordcloud')
plt.imshow(image)
plt.show()python
```

### Demo

根据飙升榜歌曲《小雨天气》前10页评论生成的词云

<img src="wordcloud.png" alt="wordcloud" style="zoom:10%;" />}