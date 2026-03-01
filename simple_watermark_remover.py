import torch
import numpy as np
import cv2
import os
import folder_paths
import torch.nn.functional as F

class SimpleWatermarkRemover:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "mask": ("MASK",),
                "algorithm": (["LAMA"], {"default": "LAMA"}),
                "help": (["(Click for Help / 点击查看帮助)"], {"default": "(Click for Help / 点击查看帮助)"}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "remove_watermark"
    CATEGORY = "image/processing"

    def _pad_tensor(self, img, mask, mod=8):
        # Pad spatial dimensions to multiples of mod (for LaMa)
        _, _, h, w = img.shape
        out_h = (h + mod - 1) // mod * mod
        out_w = (w + mod - 1) // mod * mod
        pad_h = out_h - h
        pad_w = out_w - w
        if pad_h > 0 or pad_w > 0:
            img = F.pad(img, (0, pad_w, 0, pad_h), mode='reflect')
            mask = F.pad(mask, (0, pad_w, 0, pad_h), value=0)
        return img, mask, h, w

    def remove_watermark(self, image, mask, algorithm, help):
        # image shape is [B, H, W, C]
        # mask shape is [B, H, W] or [H, W]
        
        batch_size = image.shape[0]
        result_images = []
        
        # Find big-lama.pt model
        model_dir = os.path.join(folder_paths.models_dir, "lama")
        model_path = os.path.join(model_dir, "big-lama.pt")
        
        if not os.path.exists(model_path):
            print(f"[SimpleWatermarkRemover] LaMa model not found at {model_path}. Downloading...")
            os.makedirs(model_dir, exist_ok=True)
            
            # Using a reliable download link for the TorchScript model
            download_url = "https://huggingface.co/fashn-ai/LaMa/resolve/main/big-lama.pt"
            
            try:
                import urllib.request
                
                # Add common headers to avoid being blocked by some servers
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                urllib.request.install_opener(opener)
                
                def download_progress(block_num, block_size, total_size):
                    if total_size > 0:
                        percent = int(block_num * block_size * 100 / total_size)
                        if percent % 10 == 0:
                            print(f"\r[SimpleWatermarkRemover] Downloading big-lama.pt... {percent}%", end="")
                            
                print(f"Downloading from: {download_url}")
                urllib.request.urlretrieve(download_url, model_path, download_progress)
                print(f"\n[SimpleWatermarkRemover] Download complete! Saved to {model_path}")
            except Exception as e:
                # Clean up partial file if download failed to avoid corruption
                if os.path.exists(model_path):
                    os.remove(model_path)
                    
                error_msg = str(e)
                advice = ""
                if "retrieval incomplete" in error_msg.lower():
                    advice = "\n[提示] 下载在最后关头中断了！这通常是网络极其不稳定导致的。强烈建议使用浏览器手动下载链接并放置文件。"
                elif "10061" in error_msg or "10060" in error_msg or "timeout" in error_msg.lower():
                    advice = "\n[提示] 连接被拒绝或超时，可能是网络限制。请检查代理设置或尝试手动下载。"
                elif "404" in error_msg:
                    advice = "\n[提示] 下载链接失效 (404)。请联系插件作者更新。"
                
                raise RuntimeError(f"Failed to auto-download big-lama.pt. {advice}\n"
                                 f"Click this link to download manually: {download_url}\n"
                                 f"Then place it in: {model_path}\n"
                                 f"Original Error: {e}")
        
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = torch.jit.load(model_path, map_location='cpu')
        model.eval()
        model.to(device)
        
        with torch.no_grad():
            for i in range(batch_size):
                img_tensor = image[i]
                # To [1, C, H, W]
                img_in = img_tensor.permute(2, 0, 1).unsqueeze(0).to(device) 
                
                if len(mask.shape) == 3:
                    m_idx = i if i < mask.shape[0] else -1
                    m_tensor = mask[m_idx]
                else:
                    m_tensor = mask
                
                # To [1, 1, H, W]
                mask_in = m_tensor.unsqueeze(0).unsqueeze(0).to(device) 
                
                if mask_in.shape[2:] != img_in.shape[2:]:
                    mask_in = F.interpolate(mask_in, size=img_in.shape[2:], mode='nearest')
                    
                # Binarize mask (LaMa specifically requires 0/1 mask, where 1 is the region to fill)
                mask_in = (mask_in > 0.5).float()
                
                # Pad
                img_pad, mask_pad, orig_h, orig_w = self._pad_tensor(img_in, mask_in, 8)
                
                try:
                    res = model(img_pad, mask_pad)
                    # Depending on TorchScript export, res might be tuple or raw tensor
                    if isinstance(res, tuple) or isinstance(res, list):
                        res = res[0]
                except Exception as e:
                    print(f"Error during LaMa TorchScript inference: {e}")
                    res = img_pad
                    
                # Crop black to orig size
                res = res[:, :, :orig_h, :orig_w]
                
                # Back to ComfyUI format [H, W, C] Float
                res_out = res[0].permute(1, 2, 0).cpu().clamp(0, 1)
                result_images.append(res_out)
                
        return (torch.stack(result_images, dim=0),)

NODE_CLASS_MAPPINGS = {
    "SimpleWatermarkRemover": SimpleWatermarkRemover
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SimpleWatermarkRemover": "Simple Watermark Remover"
}
