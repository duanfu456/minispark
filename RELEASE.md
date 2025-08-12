# 发布Python包指南

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