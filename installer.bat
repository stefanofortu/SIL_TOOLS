@echo off
Rem E' possibile inserire un parametro per il build della versione di interesse
Rem %0 is the program name as it was called.
Rem %1 is the first command line parameter ... and so on till %9
Rem Example: installer.bat 101

Rem aggiungere "--noconsole" per evitare che si apra il cmd all'avvio

set build_file=false

IF "%1" == "-O" (
    set build_file=true
    set file_name=SIL_tool.exe
    ECHO TC TOOL Official Release: %file_name%
)

IF "%1" == "-B" (
    set build_file=true
    set file_name=SIL_tool_beta.exe
    ECHO TC TOOL Beta Release: %file_name%
)

IF %build_file% == false (
    ECHO "WARNING: Specify if the executable is an official release (-O) or a beta release (-B)"
    EXIT /B
)



set copy_file=false
IF "%2" == "-copy" (
    set copy_file=true
) ELSE (
    ECHO INFO: Add option -copy to copy the file in web folder
)

Rem aggiungere "--noconsole" per evitare che si apra il cmd all'avvio

IF %build_file% == true (
    ECHO Building executable file:
    pyinstaller --specpath installer/build  --add-data "../../icons/*;." --icon "C:/Users/stefano.fortunati/PythonProjects/SIL_TOOLS/icons/test_new.ico" --onefile --distpath installer --clean --workpath installer/build --name %file_name% main.py
)

IF %copy_file% == true (
    copy /y installer\%file_name% ..\stefanofortu.github.io\software\
)