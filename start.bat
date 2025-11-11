@echo off
REM CosyVoice 啟動腳本 (Windows)
REM 雙擊此文件即可啟動 CosyVoice 系統

title CosyVoice 語音合成系統
chcp 65001 >nul

cd /d "%~dp0"

REM 檢查虛擬環境
if not exist "cosyvoice_env" (
    echo 🔨 首次運行，正在建立環境...
    python -m venv cosyvoice_env
    call cosyvoice_env\Scripts\activate.bat
    python -m pip install --upgrade pip setuptools wheel -q
    echo ✓ 環境建立完成
) else (
    call cosyvoice_env\Scripts\activate.bat
)

REM 啟動主程序
python start.py

pause
