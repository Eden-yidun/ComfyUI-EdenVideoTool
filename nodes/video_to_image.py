import subprocess # 用于执行ffmpeg命令
from pathlib import Path # 用于处理路径
import os # 用于处理文件
import io  # 用于处理文件
import numpy as np # 用于处理数组
from numpy import tensordot # 用于处理文件和目录
import torchaudio # 用于处理音频文件
from PIL import Image # 用于读取图像文件的Pillow库
import folder_paths # 用于获取路径


class Video_to_image: # 类名
    # 初始化方法
    def __init__(self): 
        pass 
    
    @classmethod  # 类方法,@classmethod 在 Python 中用于定义类方法，这些方法可以通过类本身调用，而不需要实例化对象。
    def INPUT_TYPES(s):  # 告诉主程序节点的输入参数。输入类型，决定节点左侧的输入参数类型
        return {
            "required": { 
                "video_path": ("STRING", {"default":"X://path/to/video.mp4",}), # 一个输入参数，输入为字符串，且有默认值
                "output_path": ("STRING", {"default":"X://path/to/output",}),
            },
        }

    RETURN_TYPES = ("STRING","STRING","INT","FLOAT",)  # 输出元组中每个元素的类型。输出类型，决定节点右侧的输出参数类型
    
    RETURN_NAMES = ("frames_path","audio_path","total_frames","fps",)  # 可选：输出元组中每个输出的名称。节点右侧的输出名称

    FUNCTION = "video_to_image" # 核心功能 ！！！ 函数入口，本质上是对输入的数据进行处理，并返回处理后的结果，再将其传给下一个节点。  要与属性 def后的函数名 名称 保持一致。入口点方法的名称。例如，如果 `FUNCTION = "execute"`，那么它将运行 Example().execute()

    OUTPUT_NODE = True  # 如果此节点是输出节点，从图中输出结果/图像。SaveImage 节点是一个例子。  后端在这些输出节点上迭代，并尝试在它们的父图正确连接时执行所有父节点。  如果不存在，则假定为 False。

    CATEGORY = "一墩视频工具EdenVideoTool" # 节点应在 UI 中出现的类别。右键的一列表显示的东西

    

    def video_to_image(self, video_path,output_path):
        
        # 提取音频
        audio_path = os.path.join(output_path, 'audio.mp3')
        audio_cmd = [
            'ffmpeg', '-i', video_path, 
            '-q:a', '0', '-map', 'a','-y', audio_path
        ]
        subprocess.run(audio_cmd)

        # 获取帧率信息
        frame_rate_cmd = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate', '-of', 'default=nokey=1:noprint_wrappers=1', str(video_path)
        ]
        frame_rate_result = subprocess.run(frame_rate_cmd, capture_output=True, text=True)
        if frame_rate_result.returncode != 0:
            print(f"Error: {frame_rate_result.stderr}")
        else:
            frame_rate_str = frame_rate_result.stdout.strip()


        # 获取时长信息
        duration_cmd = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=duration', '-of', 'default=nokey=1:noprint_wrappers=1', str(video_path)
        ]
        duration_result = subprocess.run(duration_cmd, capture_output=True, text=True)
        duration_str = duration_result.stdout.strip()

        # 处理帧率信息
        fps = None
        if frame_rate_str:
            frame_rate_parts = frame_rate_str.split('/')
            if len(frame_rate_parts) == 2:
                try:
                    numerator = int(frame_rate_parts[0])
                    denominator = int(frame_rate_parts[1])
                    fps = numerator / denominator
                except ValueError:
                    print("无法解析帧率信息")
            else:
                print("无法解析帧率信息")
        else:
            print("无法获取帧率信息")

        # 处理时长信息
        duration = None
        if duration_str:
            try:
                duration = float(duration_str)
            except ValueError:
                print("无法解析时长信息")
        else:
            print("无法获取时长信息")

        # 计算总帧数
        total_frames = None
        if fps and duration:
            total_frames = int(fps * duration)

        # 提取帧
        frames_path = os.path.join(output_path, 'frames')
        os.makedirs(frames_path, exist_ok=True)
        command = [
            'ffmpeg', '-i', video_path,  # 输入视频路径
            os.path.join(frames_path, 'frame_%04d.png')  # 输出帧路径
        ]
        subprocess.run(command) 

        # 打印信息
        print(f"序列帧图片输出路径 Frames output directory: {frames_path}")
        print(f"音频输出路径 Audio file: {audio_path}")   
        print(f"总帧数 Total frames: {total_frames}")
        print(f"帧率 Frame rate: {fps}")

        
        return (frames_path,audio_path,total_frames,fps)   # 对返回值有要求，return (xx)必须与 RETURN_TYPES 对应，否则会报错。
    


      
    """
        如果任何输入发生变化，节点将始终重新执行，
        但此方法可用于强制节点在输入不变时再次执行。
        你可以让这个节点返回一个数字或字符串。此值将与上次节点执行时返回的值进行比较，
        如果不同，节点将再次执行。
        此方法在核心仓库中用于 LoadImage 节点，它们返回图像哈希作为字符串，如果图像哈希在执行之间发生变化，
        LoadImage 节点将再次执行。
    """
    #@classmethod
    #def IS_CHANGED(s, image, string_field, int_field, float_field, print_to_screen):    # 可选方法，用于控制节点何时重新执行。输入不变的情况下，强制执行。
    #    return ""
    # 使用路由添加自定义 API 路由
# 设置 web 目录，该目录中的任何 .js 文件都将作为前端扩展加载
# WEB_DIRECTORY = "./somejs"

'''
# 使用路由添加自定义 API 路由
from aiohttp import web
from server import PromptServer

@PromptServer.instance.routes.get("/hello")
async def get_hello(request):
    return web.json_response("hello")


# 一个包含所有要导出的节点的字典
# 注意：名称应全局唯一
NODE_CLASS_MAPPINGS = {
    "Eden_video to image": Video_to_image , # 节点的类名
}

# 一个包含节点友好/人类可读标题的字典
NODE_DISPLAY_NAME_MAPPINGS = {
    "Eden_video to image": "视频转序列帧 video to image",  # 搜索节点名称 : 节点块上方显示名称
}
'''