# CosyVoice 安裝故障排除指南

## 當前問題

Python 3.14.0 是一個非常新的版本，許多 AI/ML 相關的包還沒有跟上支援，包括：
- PyTorch (目前支援到 Python 3.12)
- onnxruntime
- 其他依賴包

## 解決方案

### 選項 1: 降級到 Python 3.12 (推薦) ⭐

Python 3.12 有完整的生態系統支援，是最佳選擇。

```bash
# 1. 刪除現有虛擬環境
rm -r cosyvoice_env

# 2. 使用 Python 3.12 建立新環境（如果系統已安裝）
# 首先檢查是否有 Python 3.12
python3.12 --version

# 如果有，使用它建立虛擬環境
python3.12 -m venv cosyvoice_env

# 3. 啟動虛擬環境
.\cosyvoice_env\Scripts\Activate.ps1

# 4. 升級 pip
python -m pip install --upgrade pip

# 5. 安裝依賴
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com
```

### 選項 2: 使用 Conda (Windows 建議) 

Conda 通常處理複雜的依賴更好。

```bash
# 1. 安裝 Miniconda (如果還沒有)
# 下載: https://docs.conda.io/en/latest/miniconda.html

# 2. 建立環境（使用 Python 3.12）
conda create -n cosyvoice python=3.12 -y
conda activate cosyvoice

# 3. 安裝 PyTorch (先於 requirements.txt)
conda install pytorch torchaudio pytorch-cuda=12.1 -c pytorch -y

# 4. 安裝其他依賴
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com
```

### 選項 3: 跳過 onnxruntime (快速開始)

如果你只想快速試用基本功能，可以臨時移除有問題的依賴：

```bash
# 1. 複製 requirements.txt 並編輯
copy requirements.txt requirements_temp.txt

# 2. 用文本編輯器打開 requirements_temp.txt，移除以下行:
#    - onnxruntime-gpu==1.18.0
#    - onnxruntime==1.18.0
#    - tensorrt-cu12
#    - tensorrt-cu12-bindings
#    - tensorrt-cu12-libs

# 3. 使用修改過的文件安裝
pip install -r requirements_temp.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com
```

## 推薦步驟 (Windows)

1. **安裝 Miniconda** (最簡單)
   - 下載: https://docs.conda.io/en/latest/miniconda.html
   - 安裝時選擇「Add Miniconda to PATH」

2. **在 PowerShell 中執行**:
   ```powershell
   # 關閉並重新打開 PowerShell

   conda create -n cosyvoice python=3.12 pytorch torchaudio pytorch-cuda=12.1 -c pytorch -y
   conda activate cosyvoice
   
   cd C:\Users\swanl\Desktop\cosyvoice
   pip install -r requirements.txt
   ```

3. **驗證安裝**:
   ```bash
   python diagnose.py
   ```

## 快速檢查清單

- [ ] Python 版本是 3.12 或更低？
- [ ] PyTorch 已安裝？
- [ ] 虛擬環境已啟動？
- [ ] 所有依賴已安裝？

## 如需幫助

- 查看 [PyTorch 官方文檔](https://pytorch.org/get-started/locally/)
- 訪問 [CosyVoice 項目](https://github.com/FunAudioLLM/CosyVoice)
- 檢查 [GitHub Issues](https://github.com/FunAudioLLM/CosyVoice/issues)

---

💡 **建議**: 在生產環境中，建議使用 Python 3.11 或 3.12，以確保最佳的生態系統支援。
