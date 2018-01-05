@REM Copyright (c) 2015-2016 Software AG, Darmstadt, Germany and/or its licensors.
@REM
@REM Licensed under the Apache License, Version 2.0 (the "License");
@REM you may not use this file except in compliance with the License.
@REM You may obtain a copy of the License at
@REM
@REM     http://www.apache.org/licenses/LICENSE-2.0
@REM
@REM Unless required by applicable law or agreed to in writing, software
@REM distributed under the License is distributed on an "AS IS" BASIS,
@REM WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@REM See the License for the specific language governing permissions and
@REM limitations under the License.

@echo off

REM Fix ERRORLEVEL
dir>NUL

REM Don't pollute the calling environment
setlocal

REM Init build mode 
set suppress_svn_details=false

if "%1" == "suppress_svn_details" set suppress_svn_details=true


REM Setup the Apama Environment
IF EXIST "C:\SoftwareAG\Apama" (
    call "C:\\SoftwareAG\Apama\bin\apama_env.bat"
) ELSE IF EXIST "C:\Program Files\SoftwareAG\Apama 5.3" (
    call "C:\Program Files\SoftwareAG\Apama 5.3\bin\apama_env.bat"
) ELSE (
    goto error
)

REM --------------------
REM Ant command line
REM -----------------
set "PATH=%ANT_HOME%\bin;%PATH%"
set CLASSPATH=%ANT_HOME%\lib\ant-launcher.jar

call ant -f build.xml build
goto:eof

:error
echo Could not find Apama installation