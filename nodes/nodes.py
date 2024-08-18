import subprocess # 用于执行ffmpeg命令
from pathlib import Path # 用于处理路径
import os # 用于处理文件
import io  # 用于处理文件
import numpy as np # 用于处理数组
from numpy import tensordot # 用于处理文件和目录
import torchaudio # 用于处理音频文件
from PIL import Image # 用于读取图像文件的Pillow库
import folder_paths # 用于获取路径

##！！！以上的库下面所引用的类、函数所引用的库都需要安装


# 调用其他py文件的节点类
from .image_to_video import Image_to_video # 导入 image_to_video.py 文件中的image_to_video类
from .video_to_image import Video_to_image # 导入 video_to_image.py 文件中的video_to_image类





# 设置 web 目录，该目录中的任何 .js 文件都将作为前端扩展加载
# WEB_DIRECTORY = "./somejs"


# 使用路由添加自定义 API 路由
from aiohttp import web
from server import PromptServer

@PromptServer.instance.routes.get("/hello")
async def get_hello(request):
    return web.json_response("hello")


# 一个包含所有要导出的节点的字典
# 注意：名称应全局唯一
NODE_CLASS_MAPPINGS = {
    "Eden_image to video": Image_to_video ,# 节点的类名
    "Eden_video to image": Video_to_image , # 节点的类名
}

# 一个包含节点友好/人类可读标题的字典
NODE_DISPLAY_NAME_MAPPINGS = {
    "Eden_image to video": "序列帧转视频 image to video",# 搜索节点名称 : 节点块上方显示名称
    "Eden_video to image": "视频转序列帧 video to image",  # 搜索节点名称 : 节点块上方显示名称
}