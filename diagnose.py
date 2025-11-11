#!/usr/bin/env python3
"""
CosyVoice 簡化版測試 - 不需要 onnxruntime
如果依賴安裝失敗，可以使用這個版本測試基本功能
"""

import sys
import os
from pathlib import Path


def check_environment():
    """檢查環境"""
    print("\n" + "="*60)
    print("🔍 環境檢查")
    print("="*60)
    
    # 檢查 Python 版本
    python_version = sys.version_info
    print(f"✓ Python 版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version >= (3, 14):
        print("⚠️  注意: 你使用的是 Python 3.14+，部分包可能不相容")
    
    # 檢查必要的包
    packages = ['torch', 'torchaudio', 'transformers']
    missing = []
    
    for pkg in packages:
        try:
            module = __import__(pkg)
            version = getattr(module, '__version__', '已安裝')
            print(f"✓ {pkg}: {version}")
        except ImportError:
            print(f"✗ {pkg}: 未安裝")
            missing.append(pkg)
    
    if missing:
        print(f"\n❌ 缺少必要包: {', '.join(missing)}")
        print("請執行: pip install -r requirements.txt")
        return False
    
    return True


def create_simple_demo():
    """建立一個不需要模型的簡單演示"""
    
    print("\n" + "="*60)
    print("🎵 CosyVoice 簡單演示")
    print("="*60)
    
    sys.path.append('third_party/Matcha-TTS')
    
    try:
        import torch
        import torchaudio
        print("\n✓ PyTorch 和 torchaudio 已就緒")
        
        # 嘗試生成簡單的音頻
        print("\n📝 正在生成測試音頻...")
        
        # 建立輸出目錄
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        
        # 生成一個簡單的正弦波音頻
        sample_rate = 16000
        duration = 3  # 秒
        frequency = 440  # A4 音符
        
        t = torch.linspace(0, duration, int(sample_rate * duration))
        # 生成音頻信號
        waveform = torch.sin(2 * 3.14159 * frequency * t).unsqueeze(0)
        
        # 保存
        output_file = output_dir / 'test_sine_wave.wav'
        torchaudio.save(str(output_file), waveform, sample_rate)
        print(f"✓ 測試音頻已生成: {output_file}")
        
        # 檢查模型
        print("\n" + "-"*60)
        print("📦 模型檢查")
        print("-"*60)
        
        model_paths = [
            'pretrained_models/CosyVoice2-0.5B',
            'pretrained_models/CosyVoice-300M',
            'pretrained_models/CosyVoice-300M-SFT',
        ]
        
        models_found = False
        for model_path in model_paths:
            if Path(model_path).exists():
                print(f"✓ 找到模型: {model_path}")
                models_found = True
            else:
                print(f"✗ 未找到模型: {model_path}")
        
        if not models_found:
            print("\n💡 需要下載模型才能進行語音合成")
            print("   執行: python download_models.py")
            return False
        
        return True
        
    except ImportError as e:
        print(f"\n❌ 缺少依賴: {e}")
        return False
    except Exception as e:
        print(f"\n❌ 發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主程序"""
    print("\n🚀 CosyVoice 快速診斷工具")
    
    if not check_environment():
        print("\n❌ 環境檢查失敗")
        return
    
    if not create_simple_demo():
        print("\n⚠️  部分功能不可用")
        return
    
    print("\n" + "="*60)
    print("✅ 診斷完成!")
    print("="*60)
    print("\n📖 後續步驟:")
    print("1. 如果還沒下載模型，執行:")
    print("   python download_models.py")
    print("\n2. 模型下載完成後，執行:")
    print("   python test_tts.py       # 測試語音合成")
    print("   python demo_tts.py       # 完整演示")
    print("\n3. 或啟動 Web UI:")
    print("   python webui.py --port 50000 --model_dir pretrained_models/CosyVoice2-0.5B")


if __name__ == "__main__":
    main()
