#!/usr/bin/env python3
"""
CosyVoice 完整功能演示
支持多種語音合成模式
"""

import sys
sys.path.append('third_party/Matcha-TTS')

from pathlib import Path
import torchaudio
from typing import Optional


class CosyVoiceDemo:
    """CosyVoice 演示類"""
    
    def __init__(self, model_path: str):
        """初始化模型"""
        self.model_path = model_path
        self.output_dir = Path('output')
        self.output_dir.mkdir(exist_ok=True)
        self.cosyvoice = None
        self.sample_rate = None
    
    def load_model(self) -> bool:
        """載入模型"""
        try:
            from cosyvoice.cli.cosyvoice import CosyVoice2
            print(f"📥 載入模型: {self.model_path}...")
            self.cosyvoice = CosyVoice2(
                self.model_path,
                load_jit=False,
                load_trt=False,
                fp16=False
            )
            self.sample_rate = self.cosyvoice.sample_rate
            print(f"✓ 模型載入成功! (採樣率: {self.sample_rate}Hz)")
            return True
        except Exception as e:
            print(f"❌ 模型載入失敗: {e}")
            return False
    
    def synthesize(self, text: str, mode: str = 'basic', **kwargs) -> Optional[str]:
        """
        合成語音
        
        Args:
            text: 要合成的文本
            mode: 合成模式 ('basic', 'zero_shot', 'instruct')
            **kwargs: 其他參數
        
        Returns:
            輸出文件路徑
        """
        if not self.cosyvoice:
            print("❌ 模型未載入")
            return None
        
        try:
            print(f"\n📝 文本: {text}")
            print(f"🎵 模式: {mode}")
            print("⏳ 正在合成...")
            
            if mode == 'zero_shot':
                # 零样本合成需要提示音頻
                prompt_file = kwargs.get('prompt_file', './asset/zero_shot_prompt.wav')
                voice_prompt = kwargs.get('voice_prompt', '希望你以后能够做的比我还好呦。')
                
                if not Path(prompt_file).exists():
                    print(f"⚠️  提示文件不存在: {prompt_file}")
                    return None
                
                from cosyvoice.utils.file_utils import load_wav
                prompt_speech = load_wav(prompt_file, 16000)
                
                results = list(self.cosyvoice.inference_zero_shot(
                    text,
                    voice_prompt,
                    prompt_speech,
                    stream=False
                ))
            
            elif mode == 'instruct':
                # 指令式合成
                instruction = kwargs.get('instruction', '用標準普通話說這句話')
                prompt_file = kwargs.get('prompt_file', './asset/zero_shot_prompt.wav')
                
                if not Path(prompt_file).exists():
                    print(f"⚠️  提示文件不存在: {prompt_file}")
                    return None
                
                from cosyvoice.utils.file_utils import load_wav
                prompt_speech = load_wav(prompt_file, 16000)
                
                results = list(self.cosyvoice.inference_instruct2(
                    text,
                    instruction,
                    prompt_speech,
                    stream=False
                ))
            
            else:  # basic mode
                # 基礎合成
                results = list(self.cosyvoice.inference_zero_shot(
                    text,
                    '',
                    '',
                    stream=False
                ))
            
            # 保存結果
            output_files = []
            for i, result in enumerate(results):
                output_file = self.output_dir / f'{mode}_{len(list(self.output_dir.glob("*")))}_{i}.wav'
                torchaudio.save(str(output_file), result['tts_speech'], self.sample_rate)
                output_files.append(str(output_file))
                print(f"✓ 已保存: {output_file}")
            
            return output_files[0] if output_files else None
            
        except Exception as e:
            print(f"❌ 合成失敗: {e}")
            import traceback
            traceback.print_exc()
            return None


def main():
    """主程序"""
    print("\n" + "="*60)
    print("🎤 CosyVoice 語音合成演示")
    print("="*60)
    
    model_path = 'pretrained_models/CosyVoice2-0.5B'
    
    # 檢查模型
    if not Path(model_path).exists():
        print(f"\n❌ 模型未找到: {model_path}")
        print("\n請先下載模型:")
        print(f'python -c "from modelscope import snapshot_download; snapshot_download(\'iic/CosyVoice2-0.5B\', local_dir=\'{model_path}\')"')
        return
    
    # 初始化演示
    demo = CosyVoiceDemo(model_path)
    
    if not demo.load_model():
        return
    
    # 執行示例
    print("\n" + "-"*60)
    print("📋 測試用例")
    print("-"*60)
    
    # 示例 1: 基礎中文合成
    print("\n【示例 1】基礎中文合成")
    demo.synthesize(
        "你好，歡迎使用 CosyVoice 語音合成系統。",
        mode='basic'
    )
    
    # 示例 2: 英文合成
    print("\n【示例 2】英文合成")
    demo.synthesize(
        "Hello, this is a text-to-speech synthesis demonstration.",
        mode='basic'
    )
    
    # 示例 3: 帶情感的合成
    print("\n【示例 3】帶情感的合成")
    demo.synthesize(
        "我特別喜歡這個產品，它真的很棒！",
        mode='basic'
    )
    
    print("\n" + "="*60)
    print("✅ 所有測試完成!")
    print(f"📁 輸出文件位置: {demo.output_dir.absolute()}")
    print("="*60)


if __name__ == "__main__":
    main()
