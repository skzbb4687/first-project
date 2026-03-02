import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ===================== 1. 基础配置 =====================
# 设置中文显示（解决图表中文乱码）
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows系统
# plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # Mac系统
plt.rcParams['axes.unicode_minus'] = False

# ===================== 2. 数据加载（适配无表头的数据集） =====================
# 数据集无表头，手动指定列名（对应阿里天池UserBehavior数据集的字段）
columns = ['user_id', 'item_id', 'category_id', 'behavior_type', 'timestamp']

# ！！！重点：你的数据集路径，按之前教的改（加r或双反斜杠）
file_path = r"D:\Resource\first-project\UserBehavior.csv"

# 由于数据量太大（1亿行），先采样10万行分析（避免内存溢出）
# 如果想跑全量，把nrows=100000删掉即可（但需要足够内存）
df = pd.read_csv(
    file_path,
    names=columns,  # 手动指定列名，解决KeyError问题
    nrows=100000,   # 采样10万行，新手优先用采样数据
    encoding='utf-8'
)

# ===================== 3. 数据基本信息查看 =====================
print("数据前5行：")
print(df.head())
print("\n数据基本信息：")
print(df.info())
print("\n缺失值统计：")
print(df.isnull().sum())

# ===================== 4. 数据清洗 =====================
# 1. 转换时间戳为可读时间（现在列名正确，不会报KeyError了）
df['time'] = pd.to_datetime(df['timestamp'], unit='s')
df['date'] = df['time'].dt.date  # 提取日期
df['hour'] = df['time'].dt.hour  # 提取小时

# 2. 去除重复值
df = df.drop_duplicates()

# 3. 统一行为类型（pv=浏览，fav=收藏，cart=加购，buy=下单）
behavior_map = {'pv': 1, 'fav': 2, 'cart': 3, 'buy': 4}
df['behavior_type'] = df['behavior_type'].map(behavior_map)
# 过滤无效行为类型（只保留1-4）
df = df[df['behavior_type'].isin([1,2,3,4])]

# ===================== 5. 探索性数据分析 =====================
# 5.1 行为类型分布分析
behavior_count = df['behavior_type'].value_counts()
behavior_name = {1:'浏览', 2:'收藏', 3:'加购', 4:'下单'}
behavior_count.index = behavior_count.index.map(behavior_name)

# 绘制饼图并保存
plt.figure(figsize=(8, 6))
plt.pie(behavior_count, labels=behavior_count.index, autopct='%1.1f%%', startangle=90)
plt.title('电商用户行为类型分布（采样10万行）')
plt.savefig('behavior_distribution.png', dpi=300, bbox_inches='tight')
plt.show()

# 5.2 用户活跃时段分析
hourly_behavior = df.groupby('hour')['user_id'].count()

# 绘制折线图并保存
plt.figure(figsize=(12, 6))
sns.lineplot(x=hourly_behavior.index, y=hourly_behavior.values)
plt.title('用户活跃时段分布（采样10万行）')
plt.xlabel('小时')
plt.ylabel('行为次数')
plt.xticks(range(0,24))
plt.grid(True)
plt.savefig('hourly_behavior.png', dpi=300, bbox_inches='tight')
plt.show()

# 5.3 转化率分析（浏览→加购→下单）
view_count = len(df[df['behavior_type']==1])
cart_count = len(df[df['behavior_type']==3])
buy_count = len(df[df['behavior_type']==4])

cart_conversion = (cart_count / view_count) * 100 if view_count > 0 else 0
buy_conversion = (buy_count / cart_count) * 100 if cart_count > 0 else 0

print(f"\n转化率分析：")
print(f"浏览→加购转化率：{cart_conversion:.2f}%")
print(f"加购→下单转化率：{buy_conversion:.2f}%")

# ===================== 6. 输出分析报告 =====================
with open('analysis_report.txt', 'w', encoding='utf-8') as f:
    f.write("电商用户行为分析报告（采样10万行）\n")
    f.write("="*60 + "\n")
    f.write(f"1. 行为分布：浏览占比{behavior_count['浏览']/behavior_count.sum()*100:.1f}%，下单仅占{behavior_count['下单']/behavior_count.sum()*100:.1f}%\n")
    f.write(f"2. 活跃时段：高峰出现在{hourly_behavior.idxmax()}点，低谷在{hourly_behavior.idxmin()}点\n")
    f.write(f"3. 转化率：浏览→加购{cart_conversion:.2f}%，加购→下单{buy_conversion:.2f}%\n")

print("\n✅ 分析完成！已生成behavior_distribution.png、hourly_behavior.png、analysis_report.txt")

