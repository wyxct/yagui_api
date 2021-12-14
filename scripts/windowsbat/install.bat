@ echo off

@echo add system path
set mypath=%~dp0
set path=%mypath%;%path%
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v "Path" /t REG_EXPAND_SZ /d "%path%" /f

@echo start install [ManageService]
call nssm install ManageService %~dp0manage.exe

echo wscript.sleep 5000 > delay.vbs 
cscript //nologo delay.vbs & del delay.vbs 
@echo start [ManageService]
call nssm start ManageService

pause
