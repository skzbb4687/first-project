# 电商用户行为分析
## 项目介绍
这是我作为大二大数据专业学生的第一个GitHub项目，基于Python+Pandas对阿里天池电商用户行为数据集进行探索性分析，涵盖数据清洗、可视化、转化率分析等核心环节。

## 技术栈
- Python 3.9
- Pandas（数据处理）
- Matplotlib/Seaborn（数据可视化）

## 数据集
阿里天池公开电商用户行为数据集：https://tianchi.aliyun.com/dataset/dataDetail?dataId=649  
（注：数据集文件较大，未上传至仓库，可点击链接免费下载）

## 核心分析结果
1. 行为分布：用户浏览行为占比90%以上，下单行为占比不足1%；
2. 活跃时段：用户活跃高峰集中在晚间20-22点，凌晨4点活跃度最低；
3. 转化率：浏览→加购转化率约5%，加购→下单转化率约10%。

## 运行方法
1. 下载数据集后放入`data`文件夹；
2. 安装依赖：`pip install pandas numpy matplotlib seaborn`；
3. 运行代码：`python src/core.py`。

## 项目结构
