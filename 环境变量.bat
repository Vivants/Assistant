@echo off
setlocal enabledelayedexpansion

:: ����Ƿ��Թ���Ա�������
if "%1"=="admin" (goto gotAdmin)
mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c ""%~f0"" admin","","runas",1)(window.close)&exit
:gotAdmin


:: ���嵱ǰĿ¼�µ� Python ·���������ǵ�ǰĿ¼�µ� "python" �ļ��У�
set "DIR=%~dp0"
set "PYTHON_DIR=%DIR%Python"

:: ���·�����Ƿ���� python.exe
if not exist "%PYTHON_DIR%\python.exe" (
    echo ����Ŀ¼ "%DIR%" ��δ�ҵ� python.exe��
    pause
    exit /b 1
)

:: ��ȡ��ǰϵͳ PATH ����
for /f "tokens=2*" %%a in ('reg query "HKLM\System\CurrentControlSet\Control\Session Manager\Environment" /v Path ^| find "REG_EXPAND_SZ"') do (
    set "CURRENT_PATH=%%b"
)

:: ����Ƿ��Ѵ��ڸ�·��
echo %CURRENT_PATH% | find /i "%PYTHON_DIR%" >nul
if %errorLevel% equ 0 (
    echo ·�� "%PYTHON_DIR%" ����ϵͳ���������У�
    pause
    exit /b 0
)

:: ׷��·����ϵͳ PATH
set "NEW_PATH=%CURRENT_PATH%;%PYTHON_DIR%"
setx /m PATH "!NEW_PATH!" >nul

if %errorLevel% equ 0 (
    echo �ɹ���� "%PYTHON_DIR%" ��ϵͳ����������
    echo ע�⣺��Ҫ���������µ�¼ʹ������Ч��
) else (
    echo ���ʧ�ܣ�����Ȩ�޻�·����ʽ��
)

pause
