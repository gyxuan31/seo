import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 读取CSV文件
df = pd.read_csv('search.csv')

# 确保列名没有多余的空格
df.columns = df.columns.str.strip()

# 提取需要的列
search_word_length = df['搜索词字数']
page_views = df['浏览量(PV)']

# 绘制散点图
plt.rcParams['font.sans-serif'] = ['Kaitt', 'SimHei']
plt.figure(figsize=(10, 6))
plt.scatter(search_word_length, page_views, alpha=0.5, label='Scatter plot')

# 计算正态分布
mean, std = norm.fit(search_word_length)
x = np.linspace(min(search_word_length), max(search_word_length),100)
p = norm.pdf(x, mean, std)
print(mean)
# 绘制正态分布曲线
plt.plot(x, p * max(page_views) / max(p) *0.3, '#A9D18E', linewidth=2, label='Normal distribution fit')

ax = plt.gca()
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color('black')
    spine.set_linewidth(1.5)

# 添加图例和标签
plt.xlabel('关键词字数（字）',fontsize = 20,size = 18)
plt.ylabel('有机流量（次）',fontsize = 20,size = 18)
plt.title('关键词字数与有机流量的关系曲线',fontsize = 25)

plt.legend()

# 显示图形
plt.show()
