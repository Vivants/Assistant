@echo off
setlocal enabledelayedexpansion

:: 检查是否以管理员身份运行
if "%1"=="admin" (goto gotAdmin)
mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c ""%~f0"" admin","","runas",1)(window.close)&exit
:gotAdmin


:: 定义当前目录下的 Python 路径（假设是当前目录下的 "python" 文件夹）
set "DIR=%~dp0"
set "PYTHON_DIR=%DIR%Python"

:: 检查路径下是否存在 python.exe
if not exist "%PYTHON_DIR%\python.exe" (
    echo 错误：目录 "%DIR%" 中未找到 python.exe！
    pause
    exit /b 1
)

:: 获取当前系统 PATH 变量
for /f "tokens=2*" %%a in ('reg query "HKLM\System\CurrentControlSet\Control\Session Manager\Environment" /v Path ^| find "REG_EXPAND_SZ"') do (
    set "CURRENT_PATH=%%b"
)

:: 检查是否已存在该路径
echo %CURRENT_PATH% | find /i "%PYTHON_DIR%" >nul
if %errorLevel% equ 0 (
    echo 路径 "%PYTHON_DIR%" 已在系统环境变量中！
    pause
    exit /b 0
)

:: 追加路径到系统 PATH
set "NEW_PATH=%CURRENT_PATH%;%PYTHON_DIR%"
setx /m PATH "!NEW_PATH!" >nul

if %errorLevel% equ 0 (
    echo 成功添加 "%PYTHON_DIR%" 到系统环境变量！
    echo 注意：需要重启或重新登录使更改生效。
) else (
    echo 添加失败，请检查权限或路径格式。
)

pause
