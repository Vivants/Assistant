@echo off
setlocal enabledelayedexpansion

:: ������ԱȨ��
if "%1"=="admin" (goto gotAdmin)
mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c ""%~f0"" admin","","runas",1)(window.close)
exit /b
:gotAdmin

:: ����Ŀ¼·��
set "DIR=%~dp0"
set "PYTHON_DIR=%DIR%Python"
set "SCRIPTS_DIR=%PYTHON_DIR%\Scripts"

:: ��֤Python������
if not exist "%PYTHON_DIR%\python.exe" (
    echo ����δ�� "%PYTHON_DIR%" ���ҵ� python.exe
    pause
    exit /b 1
)
echo 1
pause
:: ��֤ScriptsĿ¼�Ƿ����
set "ADD_SCRIPTS=0"
if exist "%SCRIPTS_DIR%\" set ADD_SCRIPTS=1
if %ADD_SCRIPTS% equ 0 (
    echo ���棺δ�ҵ�ScriptsĿ¼ "%SCRIPTS_DIR%"
    choice /c yn /m "�Ƿ������"
    if errorlevel 2 exit /b 1
)

echo 2
pause
:: ��ȡ��ǰϵͳPATH
for /f "tokens=2*" %%a in ('reg query "HKLM\System\CurrentControlSet\Control\Session Manager\Environment" /v Path ^| find "REG_EXPAND_SZ"') do (
    set "CURRENT_PATH=%%b"
)

echo 3
pause
:: ·����⺯��
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
:: ������PATH
set "NEW_PATH=%CURRENT_PATH%"
call :checkPath "%PYTHON_DIR%" && echo ��⵽�Ѵ���PythonĿ¼
if %ADD_SCRIPTS% equ 1 (
    call :checkPath "%SCRIPTS_DIR%" && echo ��⵽�Ѵ���ScriptsĿ¼
)

echo 5
pause
:: ���»�������
if "!NEW_PATH!" neq "%CURRENT_PATH%" (
    :: �Ƴ���ͷ�Ķ���ֺ�
    if "!NEW_PATH:~0,1!"==";" set "NEW_PATH=!NEW_PATH:~1!"
    setx /m PATH "!NEW_PATH!" >nul
    if !errorlevel! equ 0 (
        echo �ɹ�����PATH������
        echo ���·����%PYTHON_DIR%
        if %ADD_SCRIPTS% equ 1 echo ���·����%SCRIPTS_DIR%
        echo ע�⣺��Ҫ�������¿�CMD������Ч
    ) else (
        echo ����ʧ�ܣ�����Ȩ��
    )
) else (
    echo ����·���Ѵ��ڣ������޸�
)

pause
