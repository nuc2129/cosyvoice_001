#!/usr/bin/env python3
"""
CosyVoice 快速開始指南
"""
import sys
sys.path.append('third_party/Matcha-TTS')

def check_environment():
    """檢查環境是否正確設定"""
    print("🔍 檢查環境...")
    try:
        import torch
        print(f"✓ PyTorch: {torch.__version__}")
        print(f"✓ CUDA 可用: {torch.cuda.is_available()}")
    except ImportError:
        print("✗ PyTorch 未安裝")
        return False
    
    try:
        from cosyvoice.cli.cosyvoice import CosyVoice2
        print("✓ CosyVoice 已就緒")
    except ImportError as e:
        print(f"✗ CosyVoice 載入失敗: {e}")
        return False
    
    return True

def main():
    if not check_environment():
        print("\n❌ 環境設定不完整，請先安裝依賴：")
        print("   pip install -r requirements.txt")
        return
    
    print("\n✅ 環境檢查完成！")
    print("\n📖 接下來的步驟：")
    print("1. 下載預訓練模型:")
    print("   python -c \"from modelscope import snapshot_download; snapshot_download('iic/CosyVoice2-0.5B', local_dir='pretrained_models/CosyVoice2-0.5B')\"")
    print("\n2. 執行 Web UI:")
    print("   python webui.py --port 50000 --model_dir pretrained_models/CosyVoice2-0.5B")
    print("\n3. 訪問 http://localhost:50000")

if __name__ == "__main__":
    main()
