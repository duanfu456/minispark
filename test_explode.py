import pandas as pd
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, 'build/lib')

from minispark.processors.data_processor import DataProcessor

# 创建测试数据
data = pd.DataFrame({
    '字段1': [1, 2, 3],
    '字段2': ['2-1', '3-4-5', '6'],
    '字段3': [3, 4, 5]
})

print("原始数据:")
print(data)
print()

# 创建数据处理器实例
processor = DataProcessor()

# 使用explode功能
exploded_data = processor.explode_column(data, '字段2', '-')

print("拆分后的数据:")
print(exploded_data)
print()

print(f"原始数据行数: {len(data)}")
print(f"拆分后数据行数: {len(exploded_data)}")