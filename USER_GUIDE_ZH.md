# CosyVoice 完整使用手冊

## 🎯 快速開始

### 方式 1: 雙擊啟動 (Windows)

1. 打開文件管理器
2. 進入 `c:\Users\swanl\Desktop\cosyvoice`
3. **雙擊 `start.bat`**
4. 按照菜單操作即可

### 方式 2: PowerShell 啟動

```powershell
cd C:\Users\swanl\Desktop\cosyvoice
.\start.ps1
```

### 方式 3: 手動啟動

```powershell
cd C:\Users\swanl\Desktop\cosyvoice
.\cosyvoice_env\Scripts\Activate.ps1
python start.py
```

---

## 📋 功能菜單說明

### 1. 🎵 進行語音合成

直接在命令行輸入文本，系統會自動進行語音合成，生成的音頻文件保存在 `output` 目錄。

**支援語言:**
- 中文 (簡體/繁體)
- English
- 日本語
- 한국어

### 2. 📥 下載預訓練模型

選擇要下載的模型，系統會自動從 ModelScope 下載。

**可用模型:**
- **CosyVoice2-0.5B** (推薦) - 性能最好，0.5B 參數
- **CosyVoice-300M** - 標準模型，300M 參數
- **CosyVoice-300M-SFT** - 監督微調版本

### 3. 🌐 啟動 Web UI

在瀏覽器中打開互動式 Web 界面，無需命令行操作。

**訪問地址:** http://localhost:50000

**功能:**
- 實時語音合成
- 支援多種模式
- 即時播放和下載

### 4. 🧪 運行測試

執行自動化測試，驗證系統功能是否正常。

### 5. 📊 系統診斷

檢查系統環境，診斷潛在問題。

---

## 🔧 系統設定

### 文件結構

```
cosyvoice/
├── cosyvoice_env/              # 虛擬環境 (自動建立)
├── output/                      # 輸出音頻文件
├── pretrained_models/           # 預訓練模型 (需要下載)
│   ├── CosyVoice2-0.5B/
│   ├── CosyVoice-300M/
│   └── ...
├── start.py                     # 主程序
├── start.bat                    # Windows 啟動腳本
├── start.ps1                    # PowerShell 啟動腳本
├── requirements_py314.txt       # Python 3.14 相容的依賴
├── test_tts.py                  # 測試腳本
├── demo_tts.py                  # 演示腳本
└── README.md                    # 說明文件
```

### 依賴安裝

所有依賴已自動管理，首次運行時會自動安裝。

如需重新安裝，執行:

```powershell
.\start.ps1 -install
```

---

## 💡 常見操作

### 合成特定文本

```
選擇菜單 1 > 輸入文本 > 按 Enter
```

**例子:**
```
你好，歡迎使用 CosyVoice 語音合成系統。
```

### 下載特定模型

```
選擇菜單 2 > 輸入模型編號 > 按 Enter
```

### 在 Web 上使用

```
選擇菜單 3 > 在瀏覽器中訪問 http://localhost:50000
```

---

## 🔍 故障排除

### 問題 1: 程序無法啟動

**原因:** 虛擬環境損壞或依賴缺失

**解決方案:**
```powershell
cd C:\Users\swanl\Desktop\cosyvoice
rm -r cosyvoice_env
.\start.ps1 -install
```

### 問題 2: 模型下載失敗

**原因:** 網路連接問題或 ModelScope 服務不可用

**解決方案:**
- 檢查網路連接
- 嘗試使用 VPN
- 手動從以下地址下載:
  - https://modelscope.cn/iic/CosyVoice2-0.5B

### 問題 3: 合成速度很慢

**原因:** 使用 CPU 進行推理

**解決方案:**
- 如有 NVIDIA GPU，可安裝 CUDA 版本 PyTorch
- 使用 `-q` 標誌進行快速合成

### 問題 4: Web UI 訪問失敗

**原因:** 端口已被佔用或防火牆阻止

**解決方案:**
- 檢查端口 50000 是否被佔用
- 關閉防火牆或添加例外

---

## 🎓 進階用法

### 直接調用 Python API

```python
import sys
sys.path.append('third_party/Matcha-TTS')

from cosyvoice.cli.cosyvoice import CosyVoice2
import torchaudio

# 載入模型
cosyvoice = CosyVoice2('pretrained_models/CosyVoice2-0.5B')

# 合成語音
results = list(cosyvoice.inference_zero_shot(
    '你好，世界！',
    '',  # 語音提示詞
    '',  # 語音提示
    stream=False
))

# 保存結果
torchaudio.save('output.wav', results[0]['tts_speech'], cosyvoice.sample_rate)
```

### 批量合成

建立 `batch_synthesis.py`:

```python
import sys
sys.path.append('third_party/Matcha-TTS')

from cosyvoice.cli.cosyvoice import CosyVoice2
import torchaudio
from pathlib import Path

# 載入模型
cosyvoice = CosyVoice2('pretrained_models/CosyVoice2-0.5B')

# 文本列表
texts = [
    '你好',
    '歡迎使用 CosyVoice',
    'Hello world',
]

# 批量合成
output_dir = Path('output')
for i, text in enumerate(texts):
    results = list(cosyvoice.inference_zero_shot(text, '', '', stream=False))
    if results:
        output_file = output_dir / f'batch_{i}.wav'
        torchaudio.save(str(output_file), results[0]['tts_speech'], cosyvoice.sample_rate)
        print(f"✓ 已生成: {output_file}")
```

---

## 📚 其他資源

- **官方倉庫:** https://github.com/FunAudioLLM/CosyVoice
- **官方文檔:** https://github.com/FunAudioLLM/CosyVoice/blob/main/README.md
- **示例代碼:** 查看 `examples/` 目錄
- **論文:** https://arxiv.org/abs/2412.10117 (CosyVoice 2.0)

---

## 📞 需要幫助?

1. 檢查 `INSTALL_TROUBLESHOOTING_ZH.md`
2. 查看 `diagnose.py` 的診斷結果
3. 訪問官方 GitHub Issues: https://github.com/FunAudioLLM/CosyVoice/issues

---

**祝你使用愉快! 🎉**
