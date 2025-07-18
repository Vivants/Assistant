@echo off
setlocal enabledelayedexpansion

:: 检查管理员权限
if "%1"=="admin" (goto gotAdmin)
mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c ""%~f0"" admin","","runas",1)(window.close)
exit /b
:gotAdmin

:: 设置目录路径
set "DIR=%~dp0"
set "PYTHON_DIR=%DIR%Python"
set "SCRIPTS_DIR=%PYTHON_DIR%\Scripts"

:: 验证Python主程序
if not exist "%PYTHON_DIR%\python.exe" (
    echo 错误：未在 "%PYTHON_DIR%" 中找到 python.exe
    pause
    exit /b 1
)
echo 1
pause
:: 验证Scripts目录是否存在
set "ADD_SCRIPTS=0"
if exist "%SCRIPTS_DIR%\" set ADD_SCRIPTS=1
if %ADD_SCRIPTS% equ 0 (
    echo 警告：未找到Scripts目录 "%SCRIPTS_DIR%"
    choice /c yn /m "是否继续？"
    if errorlevel 2 exit /b 1
)

echo 2
pause
:: 获取当前系统PATH
for /f "tokens=2*" %%a in ('reg query "HKLM\System\CurrentControlSet\Control\Session Manager\Environment" /v Path ^| find "REG_EXPAND_SZ"') do (
    set "CURRENT_PATH=%%b"
)

echo 3
pause
:: 路径检测函数
:checkPath
setlocal enabledelayedexpansion
set "target=%~1"
if not "%target:~-1%"=="\" set "target=%target%\"
set "ADD_FLAG=0"
echo;"!CURRENT_PATH!;" | find /i ";%target%;" >nul || (
    endlocal
    set "NEW_PATH=!NEW_PATH!;%~1"
    set "ADD_FLAG=1"
    goto :eof
)
endlocal & exit /b 0

echo 4
pause
:: 构建新PATH
set "NEW_PATH=%CURRENT_PATH%"
call :checkPath "%PYTHON_DIR%" && echo 检测到已存在Python目录
if %ADD_SCRIPTS% equ 1 (
    call :checkPath "%SCRIPTS_DIR%" && echo 检测到已存在Scripts目录
)

echo 5
pause
:: 更新环境变量
if "!NEW_PATH!" neq "%CURRENT_PATH%" (
    :: 移除开头的多余分号
    if "!NEW_PATH:~0,1!"==";" set "NEW_PATH=!NEW_PATH:~1!"
    setx /m PATH "!NEW_PATH!" >nul
    if !errorlevel! equ 0 (
        echo 成功更新PATH变量！
        echo 添加路径：%PYTHON_DIR%
        if %ADD_SCRIPTS% equ 1 echo 添加路径：%SCRIPTS_DIR%
        echo 注意：需要重启或新开CMD窗口生效
    ) else (
        echo 更新失败，请检查权限
    )
) else (
    echo 所有路径已存在，无需修改
)

pause
