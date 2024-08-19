# 中文
# ComfyUI-一墩视频工具
ComfyUI处理视频相关的节点  
主要使用ffmpeg，并且不一次性加载所有资源，比较省内存，不至于合成长视频时爆掉内存。

## 节点  
### 视频转序列帧
* 输入image_path:序列帧图片的路径。
* 输入fps：设定视频的帧率。
* 输入video_name:合成视频的名称。
* 输入output_path：合成视频的输出路径。
* 输入audio_path:合成视频的音频路径，可选。
* 输出image_path:输出刚刚输入序列帧图片的路径，方便后面进行其他处理。
* 输出output_path:输出合成视频的路径。
### 序列帧转视频 
* 输入video_path：通过图片的路径，合成视频，必选，（最大支持到1920×1080。通过一帧一帧加载，有效的节省内存。 ） 
* 输入audio_path：音频，可选。
* 输入fps：帧率，可选。  
* 输出frames_path：序列帧路径。
* 输出audio_path: 音频路径。
* 输出total_frames: 视频总帧数，整数。
* 输出fps:视频的帧率，浮点。
   
## 需求  
### ffmpeg
**ffmpeg下载**： https://ffmpeg.org/download.html    
**教程**：https://www.bilibili.com/video/BV1FB4y1n7wD/?spm_id_from=333.337.search-card.all.click&vd_source=55056672ae01e053537c956ad64231df

 ---
 ---
 ---
 
# ENGLISH
ComfyUI is a video tool that handles video-related nodes.
# ComfyUI-EdenVideoTool
It mainly uses ffmpeg and does not load all resources at once, which saves memory and prevents the app from crashing when combining long videos.
    
## Nodes
### Convert Sequence Frames to Video
* Input: image\_path: Path to the sequence frame image.
* Input: fps: Set the video frame rate.
* Input: video\_name: Name of the synthesized video.
* Input: output\_path: Output path of the synthesized video.
* Input: audio\_path: Audio path for the synthesized video (optional).
* Output: image\_path: Output the path of the input sequence frame image, for further processing.
* Output: output\_path: Output the path of the synthesized video.
### Convert Sequence Frames to Video
* Input: video\_path: Path to the sequence frame images, synthesize the video (required), (Maximum support up to 1920×1080. It loads one frame at a time, effectively saving memory.)
* Input: audio\_path: Audio (optional).
* Input: fps: Frame rate (optional).
* Output: frames\_path: Path to the sequence frame images.
* Output: audio\_path: Audio path.
* Output: total\_frames: Total number of video frames, integer.
* Output: fps: Video frame rate, floating point. ### ffmpeg
    
## requirements
**Download FFmpeg**: <https://ffmpeg.org/download.html>
**Tutorial**: <https://www.bilibili.com/video/BV1FB4y1n7wD/?spm_id_from=333.
