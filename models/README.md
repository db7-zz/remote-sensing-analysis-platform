# 本地模型权重

模型权重属于第三方资源，不进入 Git 仓库。本目录只记录获取方式和使用边界。

## YOLO11n

- 模型：Ultralytics YOLO11n 通用目标检测预训练权重。
- 本地文件：`models/weights/yolo11n.pt`。
- 获取方式：安装 `backend/requirements.txt` 后，在仓库根目录执行：

```powershell
New-Item -ItemType Directory -Path models\weights -Force
Set-Location models\weights
python -c "from ultralytics import YOLO; YOLO('yolo11n.pt')"
Set-Location ..\..
```

- 来源：Ultralytics 官方发布资源 `https://github.com/ultralytics/assets/releases/`。
- 许可：使用和分发前需遵守 Ultralytics 当前许可条款；本仓库不重新分发权重。
- 能力边界：该权重使用通用数据预训练，用于验证真实推理工程闭环，不代表遥感专项检测精度。

启动后端前也可以通过根目录 `.env` 的 `YOLO_MODEL_PATH` 指向其他兼容权重。
