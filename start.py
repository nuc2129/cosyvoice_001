#!/usr/bin/env python3
"""
CosyVoice 完整啟動系統
一鍵啟動所有功能
"""

import sys
import os
from pathlib import Path
import subprocess
import time


class CosyVoiceSystem:
    """CosyVoice 系統管理器"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.venv_dir = self.base_dir / 'cosyvoice_env'
        self.output_dir = self.base_dir / 'output'
        self.models_dir = self.base_dir / 'pretrained_models'
        self.output_dir.mkdir(exist_ok=True)
        self.models_dir.mkdir(exist_ok=True)
    
    def print_banner(self):
        """打印歡迎標題"""
        print("\n" + "="*70)
        print("🎤 CosyVoice 語音合成系統")
        print("="*70)
        print(f"📁 工作目錄: {self.base_dir}")
        print(f"🐍 虛擬環境: {self.venv_dir}")
        print(f"📦 模型目錄: {self.models_dir}")
        print("="*70 + "\n")
    
    def check_environment(self):
        """檢查環境"""
        print("🔍 環境檢查中...")
        
        checks = []
        
        # 檢查虛擬環境
        if self.venv_dir.exists():
            checks.append(("✓ 虛擬環境已就緒", True))
        else:
            checks.append(("✗ 虛擬環境不存在", False))
        
        # 檢查主要依賴
        try:
            import torch
            checks.append((f"✓ PyTorch {torch.__version__}", True))
        except:
            checks.append(("✗ PyTorch 未安裝", False))
        
        try:
            import torchaudio
            checks.append(("✓ torchaudio 已安裝", True))
        except:
            checks.append(("✗ torchaudio 未安裝", False))
        
        try:
            import transformers
            checks.append(("✓ transformers 已安裝", True))
        except:
            checks.append(("✗ transformers 未安裝", False))
        
        # 打印檢查結果
        for msg, status in checks:
            print(f"  {msg}")
        
        success = all(status for _, status in checks)
        return success
    
    def show_menu(self):
        """顯示主菜單"""
        print("\n📋 主菜單")
        print("-" * 70)
        print("1. 🎵 進行語音合成")
        print("2. 📥 下載預訓練模型")
        print("3. 🌐 啟動 Web UI")
        print("4. 🧪 運行測試")
        print("5. 📊 系統診斷")
        print("0. ❌ 退出")
        print("-" * 70)
    
    def synthesize_voice(self):
        """進行語音合成"""
        print("\n🎵 語音合成")
        print("-" * 70)
        
        text = input("請輸入要合成的文本 (中文/英文): ").strip()
        if not text:
            print("❌ 文本不能為空")
            return
        
        print(f"📝 文本: {text}")
        print("⏳ 正在初始化模型...")
        
        try:
            sys.path.insert(0, str(self.base_dir / 'third_party' / 'Matcha-TTS'))
            
            from cosyvoice.cli.cosyvoice import CosyVoice2
            from cosyvoice.utils.file_utils import load_wav
            import torchaudio
            
            # 檢查模型
            model_path = self.models_dir / 'CosyVoice2-0.5B'
            if not model_path.exists():
                print(f"\n❌ 模型未找到: {model_path}")
                print("💡 請先下載模型 (菜單選項 2)")
                return
            
            print(f"📦 載入模型: {model_path}")
            cosyvoice = CosyVoice2(str(model_path), load_jit=False, load_trt=False, fp16=False)
            
            print("⏳ 正在合成語音...")
            results = list(cosyvoice.inference_zero_shot(text, '', '', stream=False))
            
            if results:
                timestamp = int(time.time())
                output_file = self.output_dir / f'output_{timestamp}.wav'
                torchaudio.save(str(output_file), results[0]['tts_speech'], cosyvoice.sample_rate)
                print(f"✓ 語音合成完成!")
                print(f"💾 輸出文件: {output_file}")
                print(f"📊 採樣率: {cosyvoice.sample_rate} Hz")
            else:
                print("❌ 合成失敗")
        
        except Exception as e:
            print(f"❌ 錯誤: {e}")
            import traceback
            traceback.print_exc()
    
    def download_models(self):
        """下載模型"""
        print("\n📥 模型下載")
        print("-" * 70)
        
        try:
            from modelscope import snapshot_download
        except ImportError:
            print("❌ modelscope 未安裝")
            print("💡 請執行: pip install modelscope")
            return
        
        models = {
            '1': ('CosyVoice2-0.5B', 'iic/CosyVoice2-0.5B'),
            '2': ('CosyVoice-300M', 'iic/CosyVoice-300M'),
            '3': ('CosyVoice-300M-SFT', 'iic/CosyVoice-300M-SFT'),
        }
        
        print("\n可用模型:")
        for key, (name, _) in models.items():
            print(f"  {key}. {name}")
        
        choice = input("\n選擇模型 (1-3): ").strip()
        
        if choice not in models:
            print("❌ 無效選擇")
            return
        
        name, model_id = models[choice]
        local_dir = self.models_dir / name
        
        if local_dir.exists():
            print(f"✓ 模型已存在: {local_dir}")
            return
        
        print(f"\n⏳ 下載 {name}...")
        try:
            snapshot_download(model_id, local_dir=str(local_dir))
            print(f"✓ 下載完成: {local_dir}")
        except Exception as e:
            print(f"❌ 下載失敗: {e}")
    
    def launch_webui(self):
        """啟動 Web UI"""
        print("\n🌐 啟動 Web UI")
        print("-" * 70)
        
        # 檢查模型
        model_path = self.models_dir / 'CosyVoice2-0.5B'
        if not model_path.exists():
            print(f"❌ 模型未找到: {model_path}")
            print("💡 請先下載模型 (菜單選項 2)")
            return
        
        print(f"✓ 模型已找到: {model_path}")
        print(f"⏳ 啟動 Web UI...")
        print("🌐 訪問 http://localhost:50000")
        print("\n💡 按 Ctrl+C 停止服務\n")
        
        try:
            webui_script = self.base_dir / 'webui.py'
            if not webui_script.exists():
                print(f"❌ webui.py 不存在")
                return
            
            # 執行 webui
            python_exe = self.venv_dir / 'Scripts' / 'python.exe'
            subprocess.run(
                [str(python_exe), str(webui_script), '--port', '50000', 
                 '--model_dir', str(model_path)],
                cwd=str(self.base_dir)
            )
        except KeyboardInterrupt:
            print("\n✓ Web UI 已停止")
        except Exception as e:
            print(f"❌ 啟動失敗: {e}")
    
    def run_tests(self):
        """運行測試"""
        print("\n🧪 運行測試")
        print("-" * 70)
        
        test_file = self.base_dir / 'test_tts.py'
        if not test_file.exists():
            print(f"❌ test_tts.py 不存在")
            return
        
        try:
            python_exe = self.venv_dir / 'Scripts' / 'python.exe'
            subprocess.run([str(python_exe), str(test_file)], cwd=str(self.base_dir))
        except Exception as e:
            print(f"❌ 測試失敗: {e}")
    
    def diagnose(self):
        """系統診斷"""
        print("\n📊 系統診斷")
        print("-" * 70)
        
        diagnose_file = self.base_dir / 'diagnose.py'
        if not diagnose_file.exists():
            print(f"❌ diagnose.py 不存在")
            return
        
        try:
            python_exe = self.venv_dir / 'Scripts' / 'python.exe'
            subprocess.run([str(python_exe), str(diagnose_file)], cwd=str(self.base_dir))
        except Exception as e:
            print(f"❌ 診斷失敗: {e}")
    
    def run(self):
        """主循環"""
        self.print_banner()
        
        if not self.check_environment():
            print("\n❌ 環境檢查不完整")
            print("💡 請確保所有依賴已安裝")
            print("   執行: pip install -r requirements_py314.txt")
            input("\n按 Enter 鍵退出...")
            return
        
        print("\n✓ 環境檢查完成!\n")
        
        while True:
            self.show_menu()
            choice = input("請選擇操作 (0-5): ").strip()
            
            if choice == '1':
                self.synthesize_voice()
            elif choice == '2':
                self.download_models()
            elif choice == '3':
                self.launch_webui()
            elif choice == '4':
                self.run_tests()
            elif choice == '5':
                self.diagnose()
            elif choice == '0':
                print("\n👋 再見!")
                break
            else:
                print("❌ 無效選擇，請重試")
            
            input("\n按 Enter 鍵繼續...")


def main():
    """主程序入口"""
    try:
        system = CosyVoiceSystem()
        system.run()
    except KeyboardInterrupt:
        print("\n\n👋 系統已退出")
    except Exception as e:
        print(f"\n❌ 致命錯誤: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
