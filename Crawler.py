from selenium import webdriver
import os
import re
import time
import jieba
import wordcloud
# import imageio
from PIL import Image
import matplotlib.pyplot as plt

# driver = webdriver.Chrome(executable_path="chromedriver")
driver = webdriver.Edge()
# driver = webdriver.Safari()
driver.get('https://music.163.com/#/song?id=1889702364')
# 定位iframe
driver.switch_to.frame(0)
# 滚动条置底
js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight'
driver.execute_script(js)
# 删除评论
commentpath = 'comments.txt'
if os.path.exists(commentpath):
    os.remove(commentpath)
# 删除词云
imagepath = 'wordcloud.png'
if os.path.exists(imagepath):
    os.remove(imagepath)
# 循环读取页数
for click in range(10):
    divs = driver.find_elements_by_css_selector('.itm')
    for div in divs:
        cnt = div.find_element_by_css_selector('.cnt.f-brk').text
        cnt = cnt.replace('\n', ' ')
        cnt = re.findall('：(.*)', cnt)[0]
        print(cnt)
        with open('comments.txt', mode='a', encoding='utf-8') as f:
            f.write(cnt + '\n')

    driver.find_element_by_css_selector('.znxt').click()
    time.sleep(0.5)

driver.quit()
# 读取评论
file = open('comments.txt', encoding='utf-8')
txt = file.read()
# 分词
txt_list = jieba.lcut(txt)
# print("分词结果：", txt_list)
txt_str = " ".join(txt_list)
print("合并分词：", txt_list)
# img = imageio.imread("sharp.png")
# 词云
img = Image.open("sharp.png")
wc = wordcloud.WordCloud(
    collocations=False,
    width=500,
    height=400,
    background_color='white',
    font_path='/Library/Fonts/Arial Unicode.ttf',
    scale=15,
    # mask=img,
    stopwords=set([line.strip() for line in open('stopwords.txt', mode='r').readlines()])
)
print("正在制作词云图...")
wc.generate(txt_str)
wc.to_file("wordcloud.png")
print("词云制作完成")
# 显示
# imageio.imopen("wordcloud.png", io_mode="r")
image = Image.open('wordcloud.png')
plt.figure('wordcloud')
plt.imshow(image)
plt.show()
