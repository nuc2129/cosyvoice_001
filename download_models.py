#!/usr/bin/env python3
"""
下載 CosyVoice 預訓練模型
"""

import sys
from pathlib import Path


def download_models():
    """下載所有推薦的模型"""
    
    print("\n" + "="*60)
    print("📥 CosyVoice 模型下載工具")
    print("="*60)
    
    models = {
        'CosyVoice2-0.5B': 'iic/CosyVoice2-0.5B',
        'CosyVoice-300M': 'iic/CosyVoice-300M',
        'CosyVoice-300M-SFT': 'iic/CosyVoice-300M-SFT',
        'CosyVoice-ttsfrd': 'iic/CosyVoice-ttsfrd',
    }
    
    try:
        from modelscope import snapshot_download
    except ImportError:
        print("❌ modelscope 未安裝")
        print("請執行: pip install modelscope")
        return False
    
    print("\n可用的模型:")
    for i, (name, model_id) in enumerate(models.items(), 1):
        print(f"  {i}. {name:20} ({model_id})")
    
    print("\n🎯 推薦: 優先下載 CosyVoice2-0.5B (性能最好)")
    
    print("\n選擇要下載的模型 (輸入編號，多個用逗號分隔，或留空下載全部):")
    choice = input(">>> ").strip()
    
    if not choice:
        selected = list(models.items())
    else:
        try:
            indices = [int(x.strip()) - 1 for x in choice.split(',')]
            selected = [list(models.items())[i] for i in indices if 0 <= i < len(models)]
        except (ValueError, IndexError):
            print("❌ 輸入無效")
            return False
    
    # 建立輸出目錄
    model_dir = Path('pretrained_models')
    model_dir.mkdir(exist_ok=True)
    
    # 下載模型
    print("\n" + "-"*60)
    for name, model_id in selected:
        local_dir = model_dir / name
        print(f"\n📥 下載 {name}...")
        print(f"   位置: {local_dir}")
        
        # 檢查是否已存在
        if local_dir.exists():
            print(f"   ✓ 模型已存在，跳過下載")
            continue
        
        try:
            print(f"   ⏳ 下載中...")
            snapshot_download(model_id, local_dir=str(local_dir))
            print(f"   ✓ 下載完成")
        except Exception as e:
            print(f"   ❌ 下載失敗: {e}")
            print(f"   💡 可以手動從以下地址下載:")
            print(f"      https://modelscope.cn/{model_id}")
    
    print("\n" + "="*60)
    print("✅ 下載完成!")
    print("\n接下來可以執行:")
    print("  python test_tts.py        # 運行基礎測試")
    print("  python demo_tts.py        # 運行完整演示")
    print("  python webui.py --port 50000 --model_dir pretrained_models/CosyVoice2-0.5B")
    print("="*60)


if __name__ == "__main__":
    download_models()
