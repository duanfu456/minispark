import pandas as pd
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from minispark.processors.data_processor import DataProcessor

# 创建测试数据
data = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'salary': [50000, 60000, 70000],
    'department': ['IT', 'HR', 'Finance']
})

print("原始数据:")
print(data)
print()

# 定义处理整行数据的函数
def process_row(row):
    print(f"处理行: {row}")
    # 根据年龄和部门计算奖金
    bonus_rate = 0.1 if row['age'] > 30 else 0.05
    dept_bonus = 5000 if row['department'] == 'IT' else 0
    result = row['salary'] * bonus_rate + dept_bonus
    print(f"计算结果: {row['salary']} * {bonus_rate} + {dept_bonus} = {result}")
    return result

print("手动计算预期结果:")
for i, row in data.iterrows():
    bonus_rate = 0.1 if row['age'] > 30 else 0.05
    dept_bonus = 5000 if row['department'] == 'IT' else 0
    expected = row['salary'] * bonus_rate + dept_bonus
    print(f"{row['name']}: {row['salary']} * {bonus_rate} + {dept_bonus} = {expected}")

print()

# 初始化处理器
processor = DataProcessor()

# 应用函数，不指定具体列
result = processor.apply_custom_function(
    data, 
    None,  # 不指定列，传入整行
    process_row, 
    'bonus'
)

print("实际结果:")
print(result)