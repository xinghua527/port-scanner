# 端口扫描工具 (Port Scanner)

## ✨ 介绍
这是一个基于 Python 的多线程端口扫描工具，支持：
- **多线程并发扫描**
- **支持端口范围 / 端口列表**
- **探测端口对应的服务**
- **获取 Banner 信息**

## 🚀 安装
运行以下命令安装所需依赖：
```sh
pip install -r requirements.txt
```
如果pip安装依赖出现问题, 可以使用下面命令尝试安装依赖
```sh
python -m pip install -r requirements.txt
```

## 🔍 使用方法
```sh
python port-scan.py
```
```sh
运行示例：
python port-scan.py
[?] 请输入目标 (格式: 主机 端口范围)
示例: 127.0.0.1 80-100 / 192.168.1.1 22,80,443 / 172.16.1.2 80
» 127.0.0.1 1-100
```