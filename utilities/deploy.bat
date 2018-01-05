@ECHO OFF
REM
REM COPYRIGHT NOTICE
REM ----------------
REM Copyright (c) 2017 Software AG, Darmstadt, Germany and/or its licensors.
REM
REM Licensed under the Apache License, Version 2.0 (the "License");
REM you may not use this file except in compliance with the License.
REM You may obtain a copy of the License at
REM
REM     http://www.apache.org/licenses/LICENSE-2.0
REM
REM Unless required by applicable law or agreed to in writing, software
REM distributed under the License is distributed on an "AS IS" BASIS,
REM WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
REM See the License for the specific language governing permissions and
REM limitations under the License.


REM **********************************************************
REM ** NOTE: YOU MAY NEED TO MODIFY THE PATH BELOW TO POINT **
REM **       TO THE CORRECT APAMA INSTALLATION LOCATION     **
REM **********************************************************
call "C:\SoftwareAG\Apama\bin\apama_env.bat"
REM **********************************************************


REM **********************************************************
REM ** DO NOT MODIFY THE LINES BELOW                        **
REM **********************************************************
@ECHO OFF

set JAVA_EXE=java
set ANT_HOME=%ANT_HOME%
set CLASSPATH=%ANT_HOME%/lib/ant-launcher.jar


REM Don't pollute the calling environment
setlocal

"%JAVA_EXE%" -classpath "%CLASSPATH%" -Dant.home="%ANT_HOME%" org.apache.tools.ant.launch.Launcher -f "%~dp0\utilities\build.xml" deploy

pause

REM **********************************************************
