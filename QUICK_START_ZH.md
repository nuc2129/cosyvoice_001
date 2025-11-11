# CosyVoice 完整系統 - 快速開始

## ✅ 系統已準備好！

你的 CosyVoice 語音合成系統已完全配置，現在可以使用了！

## 🚀 立即開始 (3 種方式)

### 方式 1️⃣: 最簡單 - 雙擊啟動

1. 打開 Windows 文件管理器
2. 進入資料夾: `C:\Users\swanl\Desktop\cosyvoice`
3. **雙擊 `start.bat` 文件**
4. 根據提示操作

```
💡 提示: 如果看到安全警告，點擊「運行」即可
```

---

### 方式 2️⃣: PowerShell

在 PowerShell 中執行:

```powershell
cd C:\Users\swanl\Desktop\cosyvoice
.\start.ps1
```

---

### 方式 3️⃣: 命令提示符 (CMD)

在命令提示符中執行:

```cmd
cd C:\Users\swanl\Desktop\cosyvoice
start.bat
```

---

## 📋 系統菜單功能

啟動後會出現以下菜單:

```
📋 主菜單
────────────────────────────────────────────────────────────────────
1. 🎵 進行語音合成         - 輸入文本，系統自動合成語音
2. 📥 下載預訓練模型       - 下載 AI 模型（首次使用必需）
3. 🌐 啟動 Web UI          - 在瀏覽器中使用圖形界面
4. 🧪 運行測試             - 驗證系統功能
5. 📊 系統診斷             - 檢查環境設定
0. ❌ 退出                 - 關閉程序
────────────────────────────────────────────────────────────────────
```

---

## 📝 首次使用步驟

### 第 1 步: 下載模型 (5-15 分鐘)

```
選擇菜單: 2
選擇模型: 1 (推薦 CosyVoice2-0.5B)
等待下載完成
```

**說明:** 這是必要的 AI 模型，第一次需要下載約 1-2 GB 的文件。

### 第 2 步: 測試語音合成

```
選擇菜單: 1
輸入文本: 你好，世界！
按 Enter
```

**結果:** 合成的音頻會保存到 `output` 文件夾

### 第 3 步: 啟動 Web UI (可選)

```
選擇菜單: 3
在瀏覽器中訪問: http://localhost:50000
```

---

## 💬 使用示例

### 例子 1: 中文語音合成

```
1️⃣ 選擇菜單 1
📝 輸入文本: 收到好友從遠方寄來的生日禮物，那份意外的驚喜與深深的祝福讓我心中充滿了甜蜜的快樂。
⏳ 等待合成
💾 音頻保存至: output\output_1731394320.wav
```

### 例子 2: 英文語音合成

```
1️⃣ 選擇菜單 1
📝 輸入文本: Hello, this is a speech synthesis demonstration.
⏳ 等待合成
💾 音頻保存至: output\output_1731394321.wav
```

### 例子 3: Web UI 使用

```
3️⃣ 選擇菜單 3
🌐 訪問 http://localhost:50000
📝 在網頁上輸入文本
🎵 即時合成和播放
⬇️ 直接下載音頻文件
```

---

## 🎤 支援語言

✅ **中文**
- 簡體中文
- 繁體中文
- 方言: 粵語、四川話、上海話、天津話、武漢話等

✅ **English**
- 支援標準英文和各地口音

✅ **日本語** (日本語)

✅ **한국어** (韓文)

---

## 📁 文件說明

```
cosyvoice/
├── start.bat                    ⭐ 雙擊啟動（Windows）
├── start.ps1                    PowerShell 啟動
├── start.py                     主程序
├── output/                      📁 合成的音頻文件存放位置
├── pretrained_models/           📁 AI 模型存放位置
├── cosyvoice_env/               📁 虛擬環境（自動建立）
├── USER_GUIDE_ZH.md             📖 完整用戶指南
├── README.md                    官方文檔
└── ...其他檔案
```

---

## ⚙️ 系統要求

✅ **已滿足:**
- Python 3.14
- PyTorch 2.1.2
- 所有必要的 Python 套件

✅ **推薦:**
- 4GB+ RAM (最低)
- 8GB+ RAM (推薦)
- 2GB+ 硬碟空間 (用於模型)
- 網路連接 (用於首次下載)

---

## 🔧 故障排除

### ❌ 無法啟動？

**方案 1:** 檢查虛擬環境
```powershell
cd C:\Users\swanl\Desktop\cosyvoice
.\cosyvoice_env\Scripts\Activate.ps1
python start.py
```

**方案 2:** 重新安裝依賴
```powershell
.\start.ps1 -install
```

### ❌ 模型下載失敗？

- 檢查網路連接
- 嘗試使用 VPN
- 稍後重試

### ❌ 合成很慢？

- 這是正常的 (CPU 推理需要時間)
- 首次合成會更慢
- 之後會逐漸加速

---

## 💡 進階用法

### 批量合成腳本

建立 `batch.py`:

```python
import sys
sys.path.append('third_party/Matcha-TTS')
from cosyvoice.cli.cosyvoice import CosyVoice2
import torchaudio

cosyvoice = CosyVoice2('pretrained_models/CosyVoice2-0.5B')

texts = ['你好', '世界', 'Hello']

for i, text in enumerate(texts):
    results = list(cosyvoice.inference_zero_shot(text, '', '', stream=False))
    torchaudio.save(f'output/batch_{i}.wav', results[0]['tts_speech'], 16000)
```

執行:
```bash
python batch.py
```

---

## 📚 更多資源

- 📖 **完整指南**: 查看 `USER_GUIDE_ZH.md`
- 🐛 **故障排除**: 查看 `INSTALL_TROUBLESHOOTING_ZH.md`
- 🔍 **系統診斷**: 選擇菜單 5
- 🌐 **官方文檔**: https://github.com/FunAudioLLM/CosyVoice

---

## ✨ 功能特點

🎯 **零樣本語音合成** - 無需訓練資料即可生成任意語音
🌍 **多語言支援** - 支援中文、英文、日文、韓文等
⚡ **低延遲** - 快速語音合成
🎨 **高品質** - 自然流暢的語音輸出
🔧 **易於使用** - 圖形界面 + 命令行

---

## 🎉 祝你使用愉快！

如有任何問題，請查閱相關文檔或訪問官方倉庫。

**開始使用:** 雙擊 `start.bat` 或運行 `.\start.ps1`

---

**最後更新:** 2025年11月12日
