@echo off
REM invoking Bellatrix script withing Windows
REM %~dp0 is the path of the script
REM %* is the list of parameters

set cmd=python %~dp0bellatrix %*
echo Calling: %cmd%
%cmd%