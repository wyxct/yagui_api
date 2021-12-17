@echo off
::脚本功能
::manage程序安装并启动服务
@echo [enabel super administrator rights]
%1 %2
ver|find "5.">nul&&goto :st
mshta vbscript:createobject("shell.application").shellexecute("%~s0","goto :st","","runas",1)(window.close)&goto :eof
:st

@echo [add system path]
set mypath=%~dp0
set path=%mypath%;%path%

@echo [start TaskDispacher]
call nssm start TaskDispacher

pause
