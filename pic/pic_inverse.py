import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# 定义反函数模型
def inverse_function(x, a, b):
    return a / (x + b)

# 读取CSV文件
df = pd.read_csv('1pic.csv')
# 确保“平均访问时长”和“跳出率”列是数值型
df['平均访问时长'] = pd.to_numeric(df['平均访问时长'], errors='coerce')
df['跳出率'] = pd.to_numeric(df['跳出率'], errors='coerce')

# 删除任何包含NaN值的行
df.dropna(subset=['平均访问时长', '跳出率'], inplace=True)

# 将跳出率从百分数转换为小数
df['跳出率'] = df['跳出率'] / 100.0

# 提取“平均访问时长”和“跳出率”列
average_duration = df['平均访问时长'].values
bounce_rate = df['跳出率'].values

# 拟合反函数模型
popt, pcov = curve_fit(inverse_function, bounce_rate, average_duration)

# 获取拟合参数
a, b = popt

print(f'拟合参数: a = {a}, b = {b}')

# 可视化数据和拟合曲线
plt.rcParams['font.sans-serif'] = ['Kaitt', 'SimHei']

plt.scatter(bounce_rate*10000,average_duration, label='数据点', s=15)
x = np.linspace(min(bounce_rate), max(bounce_rate), 100)
y = inverse_function(x, a, b)

# plt.yticks(np.arange(min(average_duration), max(average_duration), 10000))
# 调整轴的边界线样式，添加外框黑线
ax = plt.gca()
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color('black')
    spine.set_linewidth(1.5)
plt.plot(x*10000, y, color = '#A9D18E', label='拟合曲线')
plt.xlabel('跳出率（s）',fontsize = 20)
plt.ylabel('平均访问时长(s)', fontsize = 20)
plt.xticks(np.arange(0, 101, 10))
plt.title('平均访问时长和跳出率的拟合曲线', fontsize = 25)
plt.show()