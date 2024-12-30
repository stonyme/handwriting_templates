# 手写体图片生成与转换

本仓库包含两个 Python 脚本：

1. **GNT 转 PNG 转换器**：convert.py 程序是将中科院 `.gnt` 文件中的手写字符提取为 `.png` 图片文件。
2. **手写体图片生成器**：generate_handwriting.py 程序利用`.gnt`转换的 png 模板生成指定文本的合成手写体图片。

---

## 中科院的手写体数据集下载地址：

官方获取连接：
http://www.nlpr.ia.ac.cn/databases/download/feature_data/HWDB1.1trn_gnt.zip
http://www.nlpr.ia.ac.cn/databases/download/feature_data/HWDB1.1tst_gnt.zip
网盘连接：https://pan.baidu.com/s/1pKaTg9CY5RB9C8m7itzSaQ
提取码：oubr

## 环境要求

运行以下命令安装所需的 Python 包：

```bash
pip install -r requirements.txt
```
