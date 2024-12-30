import cv2
import numpy as np
import os
import random
from concurrent.futures import ThreadPoolExecutor


# 加载手写模板到内存
def load_templates(template_dir):
    templates = {}
    for char_dir in os.listdir(template_dir):
        char_path = os.path.join(template_dir, char_dir)
        if os.path.isdir(char_path):
            templates[char_dir] = [
                cv2.imread(os.path.join(char_path, f), 0)
                for f in os.listdir(char_path)
                if f.endswith(".png")
            ]
    print(f"加载完成 {len(templates)} 个字符的模板。")
    return templates


# 生成单个字符的随机手写模板
def generate_char_image(templates, char, canvas, x_offset, canvas_height):
    if char not in templates:
        print(f"字符 '{char}' 没有找到模板，跳过。")
        return x_offset

    # 随机选择一个模板
    template = random.choice(templates[char])
    h, w = template.shape
    y_offset = random.randint(10, canvas_height - h - 10)  # 随机纵向位置
    canvas[y_offset : y_offset + h, x_offset : x_offset + w] = template
    return x_offset + w + random.randint(10, 20)  # 更新横向偏移


# 生成手写图片（支持多线程）
def generate_handwriting_image(templates, text, output_path):
    canvas_height = 120  # 画布高度
    canvas_width = len(text) * 60 + 40  # 根据文本长度调整画布宽度
    canvas = np.ones((canvas_height, canvas_width), dtype=np.uint8) * 255  # 白底画布

    x_offset = 20  # 起始位置偏移

    # 使用线程池并行生成字符图像
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for char in text:
            futures.append(
                executor.submit(
                    generate_char_image,
                    templates,
                    char,
                    canvas,
                    x_offset,
                    canvas_height,
                )
            )
            x_offset += 60  # 粗略预分配宽度避免线程冲突

        # 等待所有任务完成
        results = [f.result() for f in futures]

    # 保存结果
    cv2.imwrite(output_path, canvas)
    print(f"已保存手写图片：{output_path}")


# 主程序
if __name__ == "__main__":
    # 模板路径
    template_dir = "handwriting_templates"

    # 加载模板
    templates = load_templates(template_dir)

    # 输入文字
    text = "你好贵阳"

    # 输出文件
    output_path = "output_demo.png"

    # 生成图片
    generate_handwriting_image(templates, text, output_path)
