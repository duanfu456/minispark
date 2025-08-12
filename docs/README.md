# MiniSpark

MiniSpark是一个轻量级的Python库，用于从多种数据源读取数据并在本地进行高效处理，类似于Apache Spark的功能。

## 功能特性

- 多数据源支持：MySQL、DuckDB、SQLite、CSV、Excel和JSON
- 本地数据处理引擎（DuckDB/SQLite）
- 统一API接口
- 查询结果表注册与复用
- 支持自定义函数处理数据

## 安装

```bash
pip install minispark
```

对于特定数据库支持，可以安装额外的依赖：

```bash
# MySQL支持
pip install minispark[mysql]

# DuckDB支持
pip install minispark[duckdb]

# Excel支持
pip install minispark[excel]
```

## 支持的数据源

1. **关系型数据库**：
   - MySQL
   - DuckDB
   - SQLite

2. **文件格式**：
   - CSV
   - Excel (xlsx/xls)
   - JSON

## 各数据源使用示例

### CSV连接器

```python
from minispark import MiniSpark, CSVConnector
import pandas as pd

# 创建示例数据
data = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35]
})
data.to_csv('sample.csv', index=False)

# 初始化MiniSpark
spark = MiniSpark()

# 创建CSV连接器
csv_connector = CSVConnector('csv_connector')
spark.add_connector('csv', csv_connector)

# 从CSV文件加载数据
df = spark.load_data('csv', 'sample.csv', 'sample_table')
print(df)
```

**指定不同分隔符**：

```python
# 使用分号分隔符
semicolon_connector = CSVConnector('semicolon_csv', delimiter=';')

# 使用制表符分隔符
tab_connector = CSVConnector('tab_csv', delimiter='\t')

# 使用管道符分隔符
pipe_connector = CSVConnector('pipe_csv', delimiter='|')
```

### Excel连接器

```python
from minispark import MiniSpark, ExcelConnector
import pandas as pd

# 创建示例数据（包含多个工作表）
products_data = pd.DataFrame({
    'id': [1, 2, 3],
    'product': ['Laptop', 'Phone', 'Tablet'],
    'price': [1000, 500, 300]
})

orders_data = pd.DataFrame({
    'order_id': [101, 102],
    'product_id': [1, 2],
    'quantity': [2, 1]
})

# 保存为包含多个工作表的Excel文件
with pd.ExcelWriter('data.xlsx') as writer:
    products_data.to_excel(writer, sheet_name='Products', index=False)
    orders_data.to_excel(writer, sheet_name='Orders', index=False)

# 初始化MiniSpark
spark = MiniSpark()

# 方法1：创建通用Excel连接器（推荐）
excel_connector = ExcelConnector('excel_connector')
spark.add_connector('excel', excel_connector)

# 使用同一个连接器读取不同工作表
products_df = spark.load_data('excel', 'data.xlsx', 'products_table', sheet_name='Products')
orders_df = spark.load_data('excel', 'data.xlsx', 'orders_table', sheet_name='Orders')

# 方法2：创建指定默认工作表的Excel连接器
default_excel_connector = ExcelConnector('default_excel', sheet_name='Products')
spark.add_connector('default_excel', default_excel_connector)

# 使用默认工作表加载数据
products_df = spark.load_data('default_excel', 'data.xlsx', 'products_table')

# 覆盖默认工作表
orders_df = spark.load_data('default_excel', 'data.xlsx', 'orders_table', sheet_name='Orders')
```

### JSON连接器

```python
from minispark import MiniSpark, JSONConnector
import json

# 创建示例数据
data = [
    {"id": 1, "name": "Alice", "skills": ["Python", "SQL"]},
    {"id": 2, "name": "Bob", "skills": ["Java", "Docker"]},
    {"id": 3, "name": "Charlie", "skills": ["Excel", "Communication"]}
]

with open('employees.json', 'w') as f:
    json.dump(data, f)

# 初始化MiniSpark
spark = MiniSpark()

# 创建JSON连接器
json_connector = JSONConnector('json_connector')
spark.add_connector('json', json_connector)

# 从JSON文件加载数据
df = spark.load_data('json', 'employees.json', 'employees_table')
print(df)
```

### SQLite连接器

```python
from minispark import MiniSpark, SQLiteConnector
import sqlite3

# 创建示例数据库和数据
conn = sqlite3.connect('sample.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT
    )
''')
cursor.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
cursor.execute("INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com')")
conn.commit()
conn.close()

# 初始化MiniSpark
spark = MiniSpark()

# 创建SQLite连接器
sqlite_connector = SQLiteConnector('sqlite_connector', 'sample.db')
spark.add_connector('sqlite', sqlite_connector)

# 从SQLite数据库查询数据
df = spark.load_data('sqlite', 'SELECT * FROM users', 'users_table')
print(df)
```

### MySQL连接器

```python
from minispark import MiniSpark, MySQLConnector

# 初始化MiniSpark
spark = MiniSpark()

# 创建MySQL连接器
mysql_connector = MySQLConnector(
    name='mysql_connector',
    host='localhost',
    port=3306,
    user='username',
    password='password',
    database='database_name'
)
spark.add_connector('mysql', mysql_connector)

# 从MySQL数据库查询数据
df = spark.load_data('mysql', 'SELECT * FROM table_name LIMIT 10', 'mysql_table')
print(df)
```

### DuckDB连接器

```python
from minispark import MiniSpark, DuckDBConnector

# 初始化MiniSpark
spark = MiniSpark()

# 创建DuckDB连接器（内存数据库）
duckdb_connector = DuckDBConnector('duckdb_connector')
spark.add_connector('duckdb', duckdb_connector)

# 执行查询
df = spark.load_data('duckdb', 'SELECT 1 as number', 'test_table')
print(df)
```

### 跨数据源查询示例

```python
from minispark import MiniSpark, CSVConnector, JSONConnector

# 初始化MiniSpark
spark = MiniSpark()

# 添加多个数据源
csv_connector = CSVConnector('csv_connector')
json_connector = JSONConnector('json_connector')
spark.add_connector('csv', csv_connector)
spark.add_connector('json', json_connector)

# 从不同数据源加载数据
employees_df = spark.load_data('csv', 'employees.csv', 'employees')
skills_df = spark.load_data('json', 'skills.json', 'skills')

# 在本地引擎中执行跨数据源查询
result = spark.execute_query("""
    SELECT e.name, e.department, e.salary
    FROM employees e
    WHERE e.salary > 7000
    ORDER BY e.salary DESC
""", 'high_salary_employees')

print(result)
```

### 2. 本地处理引擎
- SQLite引擎：轻量级本地数据库引擎
- DuckDB引擎：高性能分析型数据库引擎

### 3. 数据处理功能
- 注册自定义函数并在数据处理中应用
- 直接应用匿名函数进行数据转换
- 使用swifter加速Pandas操作

### 4. 查询结果表注册
`execute_query`方法支持将查询结果直接注册为表，方便后续关联查询：

```python
# 将查询结果注册为新表
spark.execute_query("""
    SELECT department, AVG(salary) as avg_salary
    FROM employees
    GROUP BY department
""", table_name="department_avg")

# 后续可以直接查询已注册的表
result = spark.execute_query("SELECT * FROM department_avg WHERE avg_salary > 50000")
```

通过提供`table_name`参数，查询结果将自动注册为可重用的表。如果需要执行查询但不希望注册结果，可以设置`register=False`。

## JSON支持

MiniSpark现在支持JSON数据源，可以处理多种JSON格式：

1. 对象数组格式
2. 单个对象格式
3. 嵌套对象格式

### JSON使用示例

```python
from minispark import MiniSpark, JSONConnector

# 初始化MiniSpark
spark = MiniSpark()

# 添加JSON连接器
json_connector = JSONConnector('json')
spark.add_connector('json', json_connector)

# 从JSON文件加载数据
df = spark.load_data('json', 'data.json', 'my_table')

# 处理复杂数据类型（如数组、嵌套对象）
# 这些数据在加载时会被自动转换为字符串格式以兼容SQL引擎
```

## 运行测试

项目包含一系列测试用例，确保功能正常工作。要运行所有测试：

```bash
# 从项目根目录运行
python -m unittest discover test

# 或者使用测试运行脚本
python test/run_tests.py
```

## 配置

MiniSpark使用`config.toml`文件进行配置：

```toml
# 本地处理引擎配置
[engine]
# 引擎类型，支持 duckdb 或 sqlite
type = "duckdb"
# 数据库路径，:memory: 表示内存模式
database_path = ":memory:"

# 临时数据存储配置
[storage]
# 存储格式，支持 parquet 或 avro
format = "parquet"
```

## 依赖

- Python 3.9+
- pandas>=1.3.0
- sqlalchemy>=1.4.0
- toml>=0.10.2
- swifter>=1.0.0

可选依赖：
- pymysql>=1.0.0 (MySQL支持)
- duckdb>=0.3.0 (DuckDB支持)
- openpyxl>=3.0.0, xlrd>=2.0.0 (Excel支持)