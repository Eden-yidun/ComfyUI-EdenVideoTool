import subprocess # 用于执行ffmpeg命令
from pathlib import Path # 用于处理路径
import os

from numpy import tensordot # 用于处理文件和目录
import folder_paths
import torchaudio
from PIL import Image # 用于读取图像文件的Pillow库

class EdenVideoTool: # 类名
 
    # 初始化方法
    def __init__(self): 
        pass 
    
    @classmethod  # 类方法,@classmethod 在 Python 中用于定义类方法，这些方法可以通过类本身调用，而不需要实例化对象。
    def INPUT_TYPES(s):  # 告诉主程序节点的输入参数。输入类型，决定节点左侧的输入参数类型
        return {
            "required": { 
                "image_path": ("STRING", {"default": "X://path/to/images",}), # 一个输入参数，输入为字符串，且有默认值
                "fps": ("INT", {
                    "default": 30, 
                    "min": 1, # 最小值
                    "max": 2048, # 最大值
                    "step": 1, # 滑块的步长
                    "display": "number" # 仅 cosmetic：显示为 "number"数字 或 "slider"滑块
                }),
                "video_name": ("STRING", {
                    "multiline": False, # 如果你想让字段看起来像 ClipTextEncode 节点上的字段，则为 True
                    "default": "new_video"
                }),
                "output_path": ("STRING", {
                    "multiline": False, # 如果你想让字段看起来像 ClipTextEncode 节点上的字段，则为 True
                    "default": ".\\output"
                }),
            },
            "optional":{
                "audio":("AUDIO",),
                }
        }

    RETURN_TYPES = ("STRING","STRING")  # 输出元组中每个元素的类型。输出类型，决定节点右侧的输出参数类型
    
    RETURN_NAMES = ("image_path","output_path",)  # 可选：输出元组中每个输出的名称。节点右侧的输出名称

    FUNCTION = "image_to_video" # 核心功能 ！！！ 函数入口，本质上是对输入的数据进行处理，并返回处理后的结果，再将其传给下一个节点。  要与属性 def后的函数名 名称 保持一致。入口点方法的名称。例如，如果 `FUNCTION = "execute"`，那么它将运行 Example().execute()

    OUTPUT_NODE = True  # 如果此节点是输出节点，从图中输出结果/图像。SaveImage 节点是一个例子。  后端在这些输出节点上迭代，并尝试在它们的父图正确连接时执行所有父节点。  如果不存在，则假定为 False。

    CATEGORY = "一墩视频工具EdenVideoTool" # 节点应在 UI 中出现的类别。右键的一列表显示的东西

    

    def image_to_video(self,image_path,fps,video_name,output_path,audio=None):
        # 获取输入目录中的所有图像文件
        image_path = Path(image_path)
        image_files = sorted(image_path.glob('*.png')) + sorted(image_path.glob('*.PNG')) + sorted(image_path.glob('*.Png'))
        output_path =  f"{output_path}\{video_name}.mp4" # 将用户填入的，分开的输出目录和输出文件名合并为一个输出路径

        if not image_files:
            print(f"Files in directory: {os.listdir(image_path)}")
            raise FileNotFoundError(f"No image files found in directory: {image_path}")
        
        # 获取第一张图像的尺寸
        with Image.open(image_files[0]) as img:
            width, height = img.size
            scale = f'{width}:{height}'
            
        # 如果尺寸大于1920x1080，则缩放至1920x1080，否则保持原尺寸
        if width > 1920 or height > 1080:
            scale = '1920:1080'
        
        # 构建ffmpeg命令
        ffmpeg_cmd = [
            'ffmpeg',
            '-framerate', str(fps),
            '-f', 'image2pipe',
            '-i', 'pipe:',
            '-vf', f'scale={scale}',
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '28',
            '-pix_fmt', 'yuv420p',
            '-y',
            str(output_path)
       ]
        # 音频部分
        if audio is not None:
          # 判断是否是 Tensor 类型
           is_tensor = not isinstance(audio, dict)
           # print('#判断是否是 Tensor 类型',is_tensor,audio)
           if not is_tensor and 'waveform' in audio and 'sample_rate' in audio:
               is_tensor = True

           # 如果是 Tensor 类型，将音频转为 WAV 文件 
           if is_tensor:
               # 转为 WAV 文件
               audio_path = f"{output_path}.wav"
               torchaudio.save(audio_path, audio['waveform'].squeeze(0), audio['sample_rate'])

            # 添加音频文件
           if audio_path and Path(audio_path).exists():
               ffmpeg_cmd.extend(['-i', str(audio_path), '-c:a', 'aac'])


       # 执行ffmpeg命令
        process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try: 
            # 将图像文件逐个写入ffmpeg进程的标准输入
            for image_file in image_files:
                with open(image_file, 'rb') as f:
                    process.stdin.write(f.read())
            process.stdin.close()

            stdout, stderr = process.communicate()
            if process.returncode != 0:
                print(f"ffmpeg 执行失败，错误信息: {stderr.decode('utf-8')}")
            else:
                print(f"视频合成成功: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error writing to ffmpeg process: {e.stderr.decode('utf-8')}")       
        
        image_path = str(image_path) # 输出路径为字符串
        
        return (image_path,output_path)   # 对返回值有要求，return (xx)必须与 RETURN_TYPES 对应，否则会报错。
    


      
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
    "序列帧转视频 image to videol": EdenVideoTool # 节点的类名
}

# 一个包含节点友好/人类可读标题的字典
NODE_DISPLAY_NAME_MAPPINGS = {
    "EdenVideoTool": "序列帧转视频 image to video"  # 节点的显示名称
}
