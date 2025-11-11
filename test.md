# 改进的yolov8印章检测技术文档

标签（空格分隔）： 轻量化

---

## 一、使用环境：
需要pytorch>=1.12，且配置yolov8运行环境
额外的包：
```
pip install ultralytic
pip install timm==1.0.7 thop efficientnet_pytorch==0.7.1 einops grad-cam==1.4.8 dill==0.3.6 albumentations==1.4.11 pytorch_wavelets==1.3.0 tidecv PyWavelets -i https://pypi.tuna.tsinghua.edu.cn/simple
    
```
## 二、代码结构

 - dataset文件夹存放训练数据集。
 - runs文件夹存放着模型训练日志、目标检测模型权重和其他信息。
 - train.py 训练模型的脚本
 - test.py 对训练好的权重进行测试的脚本，会输出模型检测耗时（包括预处理+定位）和印章定位结果可视化与裁剪印章结果，保存在result文件夹中
 - main_profile.py 输出模型和模型每一层的参数,计算量的脚本
 - val.py 使用训练好的模型计算指标的脚本
 - detect.py 推理的脚本
 - export.py 导出onnx脚本
 - 模型配置文件在ultralytics/cfg/models/v8中

## 技术亮点
### CVPR2024-StarNet Backbone.
使用StarNet CVPR2024改进yolov8-backbone.
### C2f-Star.
使用StarNet CVPR2024中的StarBlock改进C2f.

### Lightweight Shared Convolutional Detection Head

轻量化检测头.
GroupNorm在FOCS论文中已经证实可以提升检测头定位和分类的性能.
通过使用共享卷积，可以大幅减少参数数量，这使得模型更轻便，特别是在资源受限的设备上.
在使用共享卷积的同时，为了应对每个检测头所检测的目标尺度不一致的问题，使用Scale层对特征进行缩放.
综合以上，我们可以让检测头做到参数量更少、计算量更少的情况下，尽可能减少精度的损失.

<img width="1059" height="821" alt="image" src="https://github.com/user-attachments/assets/b2c21a47-569b-4cb7-bdbb-3fa129f4b1a7" />

### 表格示例

| 功能 | 状态 | 说明 |
|------|------|------|
| 实时预览 | ✅ | 已完成 |
| 语法高亮 | ✅ | 已完成 |
| 导出功能 | ✅ | 已完成 |
