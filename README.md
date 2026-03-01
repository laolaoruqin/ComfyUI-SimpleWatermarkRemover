# ComfyUI-SimpleWatermarkRemover

A lightweight and powerful watermark removal node for ComfyUI using the LaMa (Large Mask Inpainting) model.

## Features
- **High Quality**: Uses the state-of-the-art LaMa model for seamless inpainting.
- **Easy to Use**: Simple input for image and mask.
- **Auto-Download**: Automatically downloads the required model (200MB) on first run.

## Installation
1. Clone this repo to your `ComfyUI/custom_nodes` folder:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ComfyUI-SimpleWatermarkRemover.git
   ```
2. Restart ComfyUI.

## Manual Model Download
If auto-download fails, manually download [big-lama.pt](https://huggingface.co/fashn-ai/LaMa/resolve/main/big-lama.pt) and place it in:
`ComfyUI/models/lama/big-lama.pt`
