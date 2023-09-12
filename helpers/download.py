import base64
import imghdr
import os
from io import BytesIO

import requests
from PIL import Image

from content_tools import settings
from content_tools.helpers import strings


def download_image(url, **kwargs):
    """
    下载图片
    参数：
    -  url : 图片的URL地址。
    -  save_directory ：可选参数，保存图片的目录，默认为基础存储目录。
    -  filename ：可选参数，保存图片的文件名，默认为None。
    -  file_format ：可选参数，保存图片的格式，默认为None。
    -  sub_directory ：可选参数，保存图片的子目录，默认为None。
    -  resize ：可选参数，调整图片尺寸的元组 (width, height)。
    """

    save_directory = kwargs.get('save_directory', settings.BASE_STORAGE_DIR)  # 保存图片的目录，默认为基础存储目录
    filename = kwargs.get('filename')  # 保存图片的文件名，默认为None
    file_format = kwargs.get('file_format')  # 保存图片的格式，默认为None
    sub_directory = kwargs.get('sub_directory')  # 保存图片的子目录，默认为None
    resize = kwargs.get('resize')  # 新增的参数：调整图片尺寸的元组 (width, height)

    if not sub_directory:
        sub_directory = strings.calculate_md5(url)  # 如果没有指定子目录，则根据URL计算子目录的路径

    save_directory = os.path.join(save_directory, sub_directory)  # 拼接保存目录和子目录路径
    os.makedirs(save_directory, exist_ok=True)  # 创建目录（如果不存在）

    response = requests.get(url)  # 发送GET请求获取图片内容

    if response.status_code == 200:  # 如果请求成功
        content_type = response.headers.get('content-type')  # 获取响应头中的content-type字段
        if not file_format:
            file_format = content_type.split('/')[-1]  # 如果没有指定图片格式，则使用content-type字段中的值
        else:
            file_format = file_format.lower()  # 否则，使用指定的图片格式

        if not filename:
            filename = 'image.' + file_format  # 如果没有指定文件名，则使用默认的文件名
        else:
            filename = filename + '.' + file_format  # 否则，使用指定的文件名和图片格式

        file_path = os.path.join(save_directory, filename)  # 拼接保存目录和文件名路径
        sub_directory = os.path.dirname(file_path)  # 获取文件所在的子目录路径
        os.makedirs(sub_directory, exist_ok=True)  # 创建子目录（如果不存在）

        if os.path.isfile(file_path):  # 如果文件已经存在
            image = Image.open(file_path)  # 打开文件
            width, height = image.size  # 获取图片的尺寸信息
            print(f"图片已存在，路径为 '{file_path}'，尺寸为 {width}x{height}")
            return {
                'file_path': file_path,  # 返回文件路径和尺寸信息的字典
                'width': width,
                'height': height
            }

        image = Image.open(BytesIO(response.content))  # 将响应内容转换为Image对象
        # 调整图片尺寸
        if resize:
            image = image.resize(resize)

        if image.mode == "P":  # 如果图片的模式是调色板模式（P模式）
            image = image.convert("RGB")  # 则转换为RGB模式

        with open(file_path, 'wb') as f:  # 打开文件，以二进制写入模式
            image.save(f, file_format.upper())  # 保存图片到文件

        width, height = image.size  # 获取保存后的图片尺寸信息
        print(f"图片已保存为 '{file_path}'，尺寸为 {width}x{height}")
        return {
            'file_path': file_path,  # 返回文件路径和尺寸信息的字典
            'width': width,
            'height': height
        }
    else:  # 如果请求失败
        print("下载图片失败")
        return {
            'file_path': None,  # 返回空文件路径和尺寸信息的字典
            'width': None,
            'height': None
        }


def download_file(url, **kwargs):
    """
    下载文件并保存到指定目录。

    参数:
    - url: 文件的URL地址。
    - save_directory: 可选参数，保存文件的目录，默认为基础存储目录。
    - filename: 可选参数，保存文件的文件名，默认为 'file'。
    - file_format: 可选参数，保存文件的格式，默认为None。
    - sub_directory: 可选参数，保存文件的子目录，默认为根据URL计算的MD5哈希值。

    返回值:
    - 如果下载成功，返回文件的完整路径。
    - 如果下载失败，返回None。
    """
    try:
        save_directory = kwargs.get('save_directory', settings.BASE_STORAGE_DIR)  # 保存文件的目录，默认为基础存储目录
        filename = kwargs.get('filename', 'file')  # 保存文件的文件名，默认为 'file'
        file_format = kwargs.get('file_format')  # 保存文件的格式，默认为None
        sub_directory = kwargs.get('sub_directory')  # 保存文件的子目录，默认为根据URL计算的MD5哈希值
        if sub_directory is not None:
            save_directory = os.path.join(save_directory, sub_directory)  # 拼接保存目录和子目录路径
        os.makedirs(save_directory, exist_ok=True)  # 创建目录（如果不存在）

        response = requests.get(url, stream=True, allow_redirects=True)  # 发送GET请求获取文件内容
        response.raise_for_status()  # 如果请求失败，抛出异常

        content_type = response.headers.get('content-type')  # 获取响应头中的content-type字段
        if not file_format:
            file_format = content_type.split('/')[-1]  # 如果没有指定文件格式，则使用content-type字段中的值
        else:
            file_format = file_format.lower()  # 否则，使用指定的文件格式
        file_path = os.path.join(save_directory, f"{filename}.{file_format}")  # 拼接保存目录和文件路径

        if os.path.isfile(file_path):  # 如果文件已经存在
            print(f"文件已存在，路径为 '{file_path}'")
            return file_path  # 直接返回文件路径

        with open(file_path, 'wb') as file:
            chunk_size = 1024 * 1024 * 10  # 按块写入文件，每块大小为10MB
            for chunk in response.iter_content(chunk_size=chunk_size):
                file.write(chunk)

        print(f"文件已保存为 '{file_path}'")
        return file_path  # 返回文件路径
    except (requests.exceptions.RequestException, OSError):
        print("下载文件失败")
        return None  # 返回None表示下载失败


def save_base64_image(base64_string, filename, force_replace=False, **kwargs):
    """
    将base64字符串解码为图片数据并保存到指定文件。
    参数:
    - base64_string: base64编码的图片字符串。
    - filename: 保存图片的文件名。
    - force_replace: 可选参数，是否强制替换同名文件，默认为False。
    - save_directory: 可选参数，保存文件的目录，默认为基础存储目录。
    返回值:
    - 如果保存成功，返回文件的完整路径。
    - 如果保存失败，返回None。
    """
    try:
        save_directory = kwargs.get('save_directory', settings.BASE_STORAGE_DIR)  # 保存文件的目录，默认为基础存储目录
        sub_directory = kwargs.get('sub_directory', '')  # 保存文件的子目录，默认为空
        save_directory = os.path.join(save_directory, sub_directory)  # 拼接保存目录和子目录路径
        os.makedirs(save_directory, exist_ok=True)  # 创建目录（如果不存在）
        image_data = base64.b64decode(base64_string.split(",")[1])  # 解码base64字符串为图片数据
        image = Image.open(BytesIO(image_data))  # 将图片数据加载到PIL图像对象中
        image_format = image.format.lower()  # 获取图片格式
        file_path = os.path.join(save_directory, f"{filename}.{image_format}")  # 拼接保存目录和文件路径
        if os.path.isfile(file_path) and not force_replace:  # 如果文件已经存在且不强制替换
            print(f"文件已存在，路径为 '{file_path}'")
            return file_path  # 直接返回文件路径
        image.save(file_path)  # 保存图像到本地文件
        print(f"文件已保存为 '{file_path}'")
        return file_path  # 返回文件路径
    except (IOError, OSError):
        print("保存图片失败")
        return None  # 返回None表示保存失败


def image_to_base64(image_path):
    """
    将本地图片转换为带有数据类型和编码方式的base64编码字符串。
    参数:
    - image_path: 图片文件的路径。
    返回值:
    - 如果转换成功，返回带有数据类型和编码方式的base64编码字符串。
    - 如果转换失败，返回None。
    """
    try:
        if not os.path.isfile(image_path):  # 如果文件不存在
            print(f"文件不存在，路径为 '{image_path}'")
            return None
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()  # 读取图片数据
        file_format = imghdr.what(None, h=image_data)  # 获取图片格式
        if not file_format:
            print(f"无法确定图片格式，路径为 '{image_path}'")
            return None
        encoded_string = f"data:image/{file_format};base64," + base64.b64encode(image_data).decode(
            "utf-8")  # 添加数据类型和编码方式
        return encoded_string
    except (IOError, OSError):
        print("转换图片失败")
        return None
