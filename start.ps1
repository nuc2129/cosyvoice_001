#!/usr/bin/env powershell
<#
CosyVoice 啟動腳本 (PowerShell)
在 PowerShell 中執行: .\start.ps1
#>

param(
    [switch]$install = $false,
    [switch]$help = $false
)

function Show-Help {
    Write-Host @"
使用方法: .\start.ps1 [選項]

選項:
    -install    重新安裝依賴
    -help       顯示此幫助信息

示例:
    .\start.ps1              # 正常啟動
    .\start.ps1 -install     # 重新安裝所有依賴
"@
}

function Initialize-Environment {
    Write-Host "🔨 初始化環境..." -ForegroundColor Cyan
    
    $venvPath = "cosyvoice_env"
    
    if (-not (Test-Path $venvPath)) {
        Write-Host "📦 建立虛擬環境..." -ForegroundColor Yellow
        python -m venv $venvPath
    }
    
    Write-Host "🚀 啟動虛擬環境..." -ForegroundColor Cyan
    & ".\cosyvoice_env\Scripts\Activate.ps1"
    
    if ($install) {
        Write-Host "📥 安裝依賴..." -ForegroundColor Yellow
        python -m pip install --upgrade pip setuptools wheel -q
        pip install -r requirements_py314.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com -q
        Write-Host "✓ 依賴安裝完成" -ForegroundColor Green
    }
}

function Start-System {
    Write-Host "`n🎤 啟動 CosyVoice 系統..." -ForegroundColor Cyan
    python start.py
}

# 主程序
if ($help) {
    Show-Help
    return
}

Initialize-Environment
Start-System
