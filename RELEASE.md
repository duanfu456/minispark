# MiniSpark 发布说明

## 版本 0.1.9 (2025-08-16)

### 新增功能

1. 增强DataProcessor的apply_custom_function方法，支持new_column_name默认为None：
   - new_column_name参数现在默认为None
   - 当new_column_name为None时，函数可以返回字典或字典列表来动态创建列或展开行
   - 函数返回字典时，字典的键会成为新列名，值会成为对应的数据
   - 函数返回字典列表时，每个字典会扩展成一行数据
   - 保持向后兼容，原有使用方式不变

## 版本 0.1.8 (2025-08-13)

### 新增功能

1. 将handle_duplicate_columns参数移至配置中管理：
   - 作为配置项，可以通过config.toml或配置字典进行设置
   - 支持通过点对象方式访问和修改（spark.config.handle_duplicate_columns）
   - 支持通过属性访问和修改（spark.handle_duplicate_columns）
   - 保持向后兼容，默认值仍为"rename"

## 版本 0.1.7 (2025-08-12)

### 新增功能

1. 增强MiniSpark配置管理，支持多种配置方式：
   - 支持通过点对象方式访问和修改配置（如spark.config.engine.type）
   - 支持使用SimpleNamespace实现嵌套配置访问
   - 保持向后兼容，原有的配置字典和配置文件方式仍然可用
   - 移除了属性风格配置访问（如spark.engine_type），统一使用点对象方式

## 版本 0.1.6 (2025-08-12)

### 新增功能

1. 增强DataProcessor的apply_custom_function方法，支持返回多个列
   - new_column_name参数现在支持字符串列表，可以同时创建多个列
   - 函数可以返回列表、元组或字典，自动展开到对应的多个列
   - 保持向后兼容，原有单列使用方式不变

2. 增强MiniSpark类，添加list_tables方法用于查看已注册的表信息
   - 提供便捷的方法查看所有已注册表的名称、形状、列名和内存占用

3. 增强DataProcessor类，支持处理后的数据自动注册到本地引擎
   - apply_function、apply_custom_function和explode_column方法现在支持table_name和register参数
   - 处理后的数据可以自动注册为新表，便于后续查询

## 版本 0.1.5 (2025-08-11)

### 新增功能

1. 简化DataProcessor的API，只保留传入整行数据的方式
   - 移除了对单列和多列参数的支持
   - apply_custom_function和apply_function方法现在只接收整行数据
   - 函数可以通过row['列名']或row.get('列名')的方式访问任意列的值

## 版本 0.1.4 (2025-08-11)

### 新增功能

1. 增强DataProcessor的apply_custom_function和apply_function方法，支持默认传入整行数据
   - 当column参数为None时，将整行数据作为Series传递给函数
   - 函数可以通过row['列名']或row.get('列名')的方式访问任意列的值
   - 保持向后兼容，原有的单列和多列使用方式不变

## 版本 0.1.3 (2025-08-11)

### 新增功能

1. 增强DataProcessor的apply_custom_function和apply_function方法，支持多列作为参数
   - column参数现在支持字符串列表，可以同时指定多个列作为函数输入
   - 多列处理时会将指定的列打包为Series传递给函数
   - 多列处理必须指定new_column_name参数以创建新列存储结果
   - 保持向后兼容，单列使用方式不变

## 版本 0.1.2 (2025-08-11)

### 新增功能

1. 增强explode_column方法，支持使用多个分隔符拆分字段
   - separator参数现在支持字符串列表，可以同时指定多个分隔符
   - 使用正则表达式处理多个分隔符的分割逻辑
   - 保持向后兼容，原有单分隔符使用方式不变

## 版本 0.1.1 (2025-08-11)

### 新增功能

1. 添加字段拆分功能，支持将包含分隔符的字段值拆分成多行
   - 在DataProcessor中添加explode_column方法
   - 支持自定义分隔符
   - 保持其他字段值不变

## 版本 0.1.0 (2025-08-02)

### 新增功能

1. 添加JSON连接器支持，可以处理多种JSON格式：
   - 对象数组格式
   - 单个对象格式
   - 嵌套对象格式

2. 增强CSV连接器功能，支持多种分隔符：
   - 逗号分隔符（默认）
   - 分号分隔符
   - 制表符分隔符
   - 管道符分隔符

3. 改进了多字符分隔符的处理机制

### 技术改进

1. 优化CSV连接器对多字符分隔符的支持，自动使用Python引擎处理
2. 改进了复杂数据类型（如数组、嵌套对象）的处理，自动转换为字符串以兼容SQL引擎
3. 增强了错误处理和日志记录
4. 改进了Excel连接器，支持在加载数据时动态指定工作表

### 文档更新

1. 添加了JSON使用示例
2. 添加了CSV分隔符使用示例
3. 更新了README文档，包含JSON支持和CSV分隔符说明
4. 在README中添加了所有连接器类型的使用示例
5. 添加了详细的示例说明文档
6. 更新了Excel连接器文档，说明如何动态指定工作表
7. 整理了测试文件，将所有测试文件移至test目录
8. 在README中添加了测试运行说明
9. 添加了CLI工具说明

## 准备工作

1. 确保已安装必要的工具：
   ```
   pip install build twine
   ```

2. 构建包：
   ```
   python -m build
   ```

3. 检查包的有效性：
   ```
   twine check dist/*
   ```

## 注册PyPI账户

1. 访问 [PyPI官网](https://pypi.org/) 并注册账户
2. 进入账户设置页面生成API令牌
3. 复制API令牌以备使用

## 上传到PyPI测试服务器

1. 首先上传到测试服务器验证：
   ```
   twine upload --repository testpypi dist/*
   ```
   
2. 当提示输入API令牌时，输入从PyPI获取的令牌

## 上传到正式PyPI服务器

### 方法一：交互式输入API令牌
```
twine upload dist/*
```
当提示输入用户名时，输入 `__token__`，当提示输入密码时，输入您的API令牌。

### 方法二：使用环境变量（推荐）
在Windows上：
```cmd
set TWINE_USERNAME=__token__
set TWINE_PASSWORD=您的API令牌
twine upload dist/*
```

在Linux/MacOS上：
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=您的API令牌
twine upload dist/*
```

## 验证发布

1. 访问PyPI网站查看包是否成功发布
2. 尝试安装自己的包：
   ```
   pip install minispqrk
   ```