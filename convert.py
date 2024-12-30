import os
import numpy as np
import struct
from PIL import Image

# 设置输入和输出路径
gnt_dir = "gnt"  # 存放 .gnt 文件的目录
output_dir = "./output_data"  # 输出的 .png 文件保存路径


def read_from_gnt_dir(gnt_dir):
    """
    从 .gnt 文件目录中读取数据。
    """

    def one_file(f):
        """
        解析一个 .gnt 文件中的内容。
        """
        header_size = 10  # .gnt 文件头大小
        while True:
            # 读取文件头
            header = np.fromfile(f, dtype="uint8", count=header_size)
            if not header.size:
                break
            # 解析文件头
            sample_size = (
                header[0] + (header[1] << 8) + (header[2] << 16) + (header[3] << 24)
            )
            tagcode = header[5] + (header[4] << 8)
            width = header[6] + (header[7] << 8)
            height = header[8] + (header[9] << 8)

            # 检查数据是否完整
            if header_size + width * height != sample_size:
                print("数据不完整，跳过...")
                break

            # 读取图片位图数据
            bitmap = np.fromfile(f, dtype="uint8", count=width * height).reshape(
                (height, width)
            )

            # 将汉字标签转换为 Unicode
            tag = struct.pack(">H", tagcode).decode("gb2312", errors="ignore")
            yield tag, bitmap

    for file_name in os.listdir(gnt_dir):
        if not file_name.endswith(".gnt"):
            continue
        file_path = os.path.join(gnt_dir, file_name)
        with open(file_path, "rb") as f:
            for tag, bitmap in one_file(f):
                yield tag, bitmap


def save_to_images(output_dir, gnt_dir):
    """
    将从 .gnt 文件中读取的数据保存为图片。
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for tag, bitmap in read_from_gnt_dir(gnt_dir):
        # 为每个汉字创建独立的文件夹
        char_dir = os.path.join(output_dir, tag)
        if not os.path.exists(char_dir):
            os.makedirs(char_dir)

        # 生成图片文件名
        image_index = len(os.listdir(char_dir)) + 1
        image_path = os.path.join(char_dir, f"{image_index}.png")

        # 保存图片
        img = Image.fromarray(bitmap)
        img.save(image_path)
        print(f"Saved: {image_path}")


if __name__ == "__main__":
    # 开始处理并保存 .png 文件
    print("开始转换 .gnt 文件为图片...")
    save_to_images(output_dir, gnt_dir)
    print("转换完成！图片已保存到:", output_dir)
