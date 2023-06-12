from flask import jsonify, current_app
from uuid import uuid4
import os

from PIL import Image as PILImage

# 支持的文件类型
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def save_file(file : PILImage.Image, category : str, quality : int = 95):
    """
    保存文件到本地并返回文件名。

    :param file: 要保存的文件。
    :param category: 文件类别, 例如“avatar”。
    :param quality: 图片质量, 0-100, 默认95。
    :return: 文件名。
    """
    # 随机生成文件名
    filename = str(uuid4()) + ".jpg"
    # 创建文件夹
    category_path = os.path.join(current_app.config['UPLOAD_FOLDER'], category)
    if not os.path.exists(category_path):
        os.makedirs(category_path)
    # 保存文件
    file.save(os.path.join(category_path, filename), quality=quality)
    return '/api/images/' + category + '/' + filename

def json_response(data : dict, code : int) -> tuple:
    """
    返回json格式的响应。

    :param data: 要返回的数据。
    :param code: HTTP状态码。
    :return: tuple, (响应数据, HTTP状态码)。
    """
    return jsonify({"code": code, "data": data}), 200