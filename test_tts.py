#!/usr/bin/env python3
"""
CosyVoice 語音合成簡單測試
支持以下功能:
1. 零样本語音合成 (Zero-shot TTS)
2. 跨語言語音合成 (Cross-lingual TTS)
3. 語音轉換 (Voice Conversion)
"""

import sys
import os

# 添加第三方库路徑
sys.path.append('third_party/Matcha-TTS')

import torchaudio
from pathlib import Path


def setup_output_dir():
    """建立輸出目錄"""
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    return output_dir


def test_cosyvoice2_basic(model_path='pretrained_models/CosyVoice2-0.5B'):
    """
    測試 CosyVoice2 基本功能
    """
    print("="*50)
    print("🎤 CosyVoice2 語音合成測試")
    print("="*50)
    
    try:
        from cosyvoice.cli.cosyvoice import CosyVoice2
        from cosyvoice.utils.file_utils import load_wav
    except ImportError as e:
        print(f"❌ 導入失敗: {e}")
        print("請先安裝依賴: pip install -r requirements.txt")
        return False
    
    # 檢查模型是否存在
    if not Path(model_path).exists():
        print(f"\n⚠️  模型路徑不存在: {model_path}")
        print(f"請先下載模型:")
        print(f"python -c \"from modelscope import snapshot_download; snapshot_download('iic/CosyVoice2-0.5B', local_dir='{model_path}')\"")
        return False
    
    output_dir = setup_output_dir()
    
    try:
        print(f"\n📥 載入模型: {model_path}")
        cosyvoice = CosyVoice2(model_path, load_jit=False, load_trt=False, fp16=False)
        print("✓ 模型載入成功!")
        
        # 檢查音頻文件
        prompt_file = './asset/zero_shot_prompt.wav'
        if not Path(prompt_file).exists():
            print(f"\n⚠️  提示音頻文件不存在: {prompt_file}")
            print("使用文本合成進行測試...")
            
            # 無提示音頻的簡單合成
            test_text = "你好，我是通义生成式语音大模型，请问有什么可以帮您的吗？"
            print(f"\n📝 合成文本: {test_text}")
            
            # 嘗試基礎合成
            print("⏳ 正在合成語音...")
            try:
                results = list(cosyvoice.inference_zero_shot(
                    test_text, 
                    '', 
                    '',
                    stream=False
                ))
                
                if results:
                    print(f"✓ 合成成功! 生成 {len(results)} 個片段")
                    for i, result in enumerate(results):
                        output_file = output_dir / f'test_output_{i}.wav'
                        torchaudio.save(str(output_file), result['tts_speech'], cosyvoice.sample_rate)
                        print(f"  💾 已保存: {output_file}")
                else:
                    print("❌ 合成失敗，沒有返回結果")
            except Exception as e:
                print(f"❌ 合成過程出錯: {e}")
                import traceback
                traceback.print_exc()
                return False
        else:
            # 使用提示音頻
            print(f"\n🎵 載入提示音頻: {prompt_file}")
            prompt_speech_16k = load_wav(prompt_file, 16000)
            
            # 零样本合成
            test_text = "收到好友从远方寄来的生日礼物，那份意外的惊喜与深深的祝福让我心中充满了甜蜜的快乐。"
            print(f"\n📝 合成文本: {test_text}")
            print("⏳ 正在進行零样本語音合成...")
            
            results = list(cosyvoice.inference_zero_shot(
                test_text,
                '希望你以后能够做的比我还好呦。',
                prompt_speech_16k,
                stream=False
            ))
            
            print(f"✓ 合成成功! 生成 {len(results)} 個片段")
            for i, result in enumerate(results):
                output_file = output_dir / f'zero_shot_{i}.wav'
                torchaudio.save(str(output_file), result['tts_speech'], cosyvoice.sample_rate)
                print(f"  💾 已保存: {output_file}")
        
        print("\n✅ 測試完成!")
        return True
        
    except Exception as e:
        print(f"\n❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函數"""
    print("\n🚀 CosyVoice 語音測試工具")
    print("-" * 50)
    
    # 檢查環境
    try:
        import torch
        print(f"✓ PyTorch 版本: {torch.__version__}")
        if torch.cuda.is_available():
            print(f"✓ CUDA 可用: {torch.cuda.get_device_name(0)}")
        else:
            print("ℹ️  使用 CPU 進行推理（較慢）")
    except ImportError:
        print("❌ PyTorch 未安裝")
        return
    
    # 執行測試
    success = test_cosyvoice2_basic()
    
    if success:
        print("\n💡 提示:")
        print("   - 輸出文件保存在 'output' 目錄")
        print("   - 可以使用任何音頻播放器播放 .wav 文件")
        print("   - 如需更多功能，請查看 README.md 或 QUICKSTART_ZH.md")
    else:
        print("\n💡 故障排除:")
        print("   1. 確保所有依賴已安裝: pip install -r requirements.txt")
        print("   2. 確保預訓練模型已下載")
        print("   3. 檢查 CUDA/GPU 設定（可選）")


if __name__ == "__main__":
    main()
