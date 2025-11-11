# CosyVoice 開發環境設定指南

## 環境設定狀態

✅ **已完成**：
- Git 倉庫連結到 GitHub (https://github.com/nuc2129/cosyvoice_001)
- Python 虛擬環境建立: `cosyvoice_env`
- 專案程式碼已從 FunAudioLLM 複製

⏳ **進行中**：
- PyTorch 依賴安裝中...

## 快速開始步驟

### 1️⃣ 啟動虛擬環境

```bash
# Windows PowerShell
.\cosyvoice_env\Scripts\Activate.ps1

# Windows CMD
cosyvoice_env\Scripts\activate.bat

# Linux/Mac
source cosyvoice_env/bin/activate
```

### 2️⃣ 安裝完整依賴

```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com
```

### 3️⃣ 下載預訓練模型

```bash
python -c "from modelscope import snapshot_download; snapshot_download('iic/CosyVoice2-0.5B', local_dir='pretrained_models/CosyVoice2-0.5B')"
```

### 4️⃣ 運行 Web UI

```bash
python webui.py --port 50000 --model_dir pretrained_models/CosyVoice2-0.5B
```

然後訪問：http://localhost:50000

## 模型選擇

推薦模型（從高到低性能）：
- **CosyVoice2-0.5B** - 最新且效果最好
- **CosyVoice-300M-SFT** - 標準預訓練模型
- **CosyVoice-300M** - 零样本語音合成
- **CosyVoice-300M-Instruct** - 指令基礎模型

## 主要功能

### CosyVoice2 支援的功能

```python
from cosyvoice.cli.cosyvoice import CosyVoice2

cosyvoice = CosyVoice2('pretrained_models/CosyVoice2-0.5B')

# 1. 零样本語音合成 (Zero-shot)
cosyvoice.inference_zero_shot(text, voice_prompt, speech_prompt)

# 2. 跨語言語音合成 (Cross-lingual)
cosyvoice.inference_cross_lingual(text, speech_prompt)

# 3. 指令式語音合成 (Instruct)
cosyvoice.inference_instruct2(text, instruction, speech_prompt)

# 4. 流式推理
cosyvoice.inference_zero_shot(text, voice_prompt, speech_prompt, stream=True)
```

## 支援的語言

- 🇨🇳 中文 (简体/繁體)
- 🇬🇧 English
- 🇯🇵 日本語
- 🇰🇷 한국어
- 方言: 粵語、四川話、上海話、天津話、武漢話等

## 常見問題

**Q: 安裝很慢怎麼辦？**
A: 使用國內鏡像：
```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com
```

**Q: CUDA 驅動問題？**
A: CosyVoice 支援 CPU 推理，只是會較慢。也可以使用 `load_jit=True` 進行 JIT 優化。

**Q: 模型文件很大，如何加快下載？**
A: 使用 modelscope SDK 或 git-lfs 下載，或使用 VPN 加速 HuggingFace。

## 文件結構

```
cosyvoice/
├── cosyvoice/          - 核心模型程式碼
├── examples/           - 訓練和推理範例
├── runtime/            - 部署相關程式碼
├── third_party/        - 第三方依賴
├── webui.py            - Web 界面
├── requirements.txt    - 依賴列表
└── README.md           - 原始文件
```

## 下一步

1. 閱讀 [官方 GitHub](https://github.com/FunAudioLLM/CosyVoice)
2. 查看 `examples/` 目錄中的完整例子
3. 訪問 [官方 Demo](https://funaudiollm.github.io/cosyvoice2/)

---
祝你開發愉快！🎉
