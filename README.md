# GUET-zhihui-time

桂电智慧英语平台刷时长脚本
----------
**使用方法**
默认使用Edge浏览器


----------


**确保本地有python环境和必要的包**
    Windows 打开命令提示符（按下 Win + R，输入 cmd）

```
python --version  //样例输出Python 3.11.13,如果没有请先安装python
```
    
安装必要的包
    
```
pip install selenium
pip install selenium webdriver-manager
``` 


**将代码中的cookie修改为自己的**
  1.获取cookie:
    登录智慧英语平台后右键选择检查,选择应用程序（绿色），点击cookie(红色)，将cookie的值（蓝色）复制粘贴到代码中。
    
<img width="722" height="420" alt="2baf6110-0a88-4dba-a161-a5eef7aff9af" src="https://github.com/user-attachments/assets/0fee8431-0d49-4ffd-9b89-0cf623612817" />

**运行代码**
```
python3 GUET_zhihui.py
```
或者直接用pycharm运行
最后结果：

<img width="685" height="455" alt="image" src="https://github.com/user-attachments/assets/aa37d5bc-b7a1-467f-b707-d733b911c424" />
