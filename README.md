# ComfyUI-SimpleWatermarkRemover

A lightweight and powerful watermark removal node for ComfyUI using the LaMa (Large Mask Inpainting) model.
一个轻量级且强大的 ComfyUI 水印去除节点，使用 LaMa (Large Mask Inpainting) 模型。

## 📖 Usage / 使用方法

### English
1. **Load Image**: Load your image using the standard Load Image node.
2. **Create Mask**: Right-click the image in the Load Image node and select **"Open in MaskEditor"**.
3. **Draw**: Paint over the watermark you want to remove and click **"Save"**.
4. **Connect**: Connect the `IMAGE` and `MASK` outputs to this node.
5. **Run**: Queue the prompt. The model will auto-download on first use.

### 中文说明
1. **加载图片**: 使用标准 Load Image 节点加载图片。
2. **创建遮罩**: 在 Load Image 节点的图片上**点击右键**，选择 **"Open in MaskEditor"**（在遮罩编辑器中打开）。
3. **涂抹**: 涂满你想去除的水印区域，点击顶部的 **"保存"** 按钮。
4. **连接**: 将 `IMAGE` 和 `MASK` 输出连接到本节点。
5. **运行**: 运行测试。模型会在第一次使用时自动下载。

---

## 🚀 Features / 功能特点
- **High Quality / 高质量**: Uses the state-of-the-art LaMa model for seamless inpainting. 使用 SOTA 级别的 LaMa 模型，实现无缝修复。
- **Minimalist / 极简**: Simplified interface with only essential inputs. 界面精简，只保留核心输入。
- **Auto-Download / 自动下载**: Automatically downloads the required model (~200MB) from Hugging Face. 第一次使用时自动从 Hugging Face 下载所需模型（约 200MB）。

## 🛠️ Installation / 安装方法
Clone this repo to your `ComfyUI/custom_nodes` folder:
将此仓库克隆到您的 `ComfyUI/custom_nodes` 文件夹下：
```bash
git clone https://github.com/laolaoruqin/ComfyUI-SimpleWatermarkRemover.git
```

## ⚠️ Manual Model Download / 手动下载模型
If auto-download fails, manually download [big-lama.pt](https://huggingface.co/fashn-ai/LaMa/resolve/main/big-lama.pt) and place it in:
如果自动下载失败，请手动下载 [big-lama.pt](https://huggingface.co/fashn-ai/LaMa/resolve/main/big-lama.pt) 并放入以下路径：

`ComfyUI/models/lama/big-lama.pt`
