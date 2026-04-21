import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
columns = ['user_id', 'item_id', 'category_id', 'behavior_type', 'timestamp']

file_path = r"D:\Resource\first-project\UserBehavior.csv"

df = pd.read_csv(
    file_path,
    names=columns, 
    nrows=100000,
    encoding='utf-8'
)

print("数据前5行：")
print(df.head())
print("\n数据基本信息：")
print(df.info())
print("\n缺失值统计：")
print(df.isnull().sum())

df['time'] = pd.to_datetime(df['timestamp'], unit='s')
df['date'] = df['time'].dt.date 
df['hour'] = df['time'].dt.hour 

#去重
df = df.drop_duplicates()

#统一行为类型
behavior_map = {'pv': 1, 'fav': 2, 'cart': 3, 'buy': 4}
df['behavior_type'] = df['behavior_type'].map(behavior_map)
#过滤
df = df[df['behavior_type'].isin([1,2,3,4])]
#行为类型分布分析
behavior_count = df['behavior_type'].value_counts()
behavior_name = {1:'浏览', 2:'收藏', 3:'加购', 4:'下单'}
behavior_count.index = behavior_count.index.map(behavior_name)
#绘图
plt.figure(figsize=(8, 6))
plt.pie(behavior_count, labels=behavior_count.index, autopct='%1.1f%%', startangle=90)
plt.title('电商用户行为类型分布（采样10万行）')
plt.savefig('behavior_distribution.png', dpi=300, bbox_inches='tight')
plt.show()
hourly_behavior = df.groupby('hour')['user_id'].count()
#绘图
plt.figure(figsize=(12, 6))
sns.lineplot(x=hourly_behavior.index, y=hourly_behavior.values)
plt.title('用户活跃时段分布（采样10万行）')
plt.xlabel('小时')
plt.ylabel('行为次数')
plt.xticks(range(0,24))
plt.grid(True)
plt.savefig('hourly_behavior.png', dpi=300, bbox_inches='tight')
plt.show()

view_count = len(df[df['behavior_type']==1])
cart_count = len(df[df['behavior_type']==3])
buy_count = len(df[df['behavior_type']==4])

cart_conversion = (cart_count / view_count) * 100 if view_count > 0 else 0
buy_conversion = (buy_count / cart_count) * 100 if cart_count > 0 else 0

print(f"\n转化率分析：")
print(f"浏览→加购转化率：{cart_conversion:.2f}%")
print(f"加购→下单转化率：{buy_conversion:.2f}%")

with open('analysis_report.txt', 'w', encoding='utf-8') as f:
    f.write("电商用户行为分析报告（采样10万行）\n")
    f.write("="*60 + "\n")
    f.write(f"1. 行为分布：浏览占比{behavior_count['浏览']/behavior_count.sum()*100:.1f}%，下单仅占{behavior_count['下单']/behavior_count.sum()*100:.1f}%\n")
    f.write(f"2. 活跃时段：高峰出现在{hourly_behavior.idxmax()}点，低谷在{hourly_behavior.idxmin()}点\n")
    f.write(f"3. 转化率：浏览→加购{cart_conversion:.2f}%，加购→下单{buy_conversion:.2f}%\n")

