---
name: Custom issue template
about: SSH Auth Socket For Git.
title: issue template ssh for Git
labels: documentation, enhancement
assignees: Andrea-MariaDB-2

---

@REM Do not use "echo off" to not affect any child calls.

@REM The goal of this script is to simplify launching `ssh-pageant` at
@REM logon, typically by dropping a shortcut into the Startup folder, so
@REM that Pageant (the PuTTY authentication agent) will always be
@REM accessible. No attempt is made to load SSH keys, since this is
@REM normally handled directly by Pageant, and no interactive shell
@REM will be launched.
@REM 
@REM The `ssh-pageant` utility is launched with the `-r` (reuse socket)
@REM option, to ensure that only a single running incarnation (per user)
@REM will be required... instead of launching a separate process for
@REM every interactive Git Bash session. A side effect of this selection
@REM is that the SSH_AUTH_SOCK environment variable *must* be set prior
@REM to running this script, with the value specifying a unix-style socket
@REM path, and needs to be consistent for all git-related processes. The
@REM easiest way to do this is to set a persistent USER environment
@REM variable, which (under Windows 7) can be done via Control Panel
@REM under System / Advanced System Settings. A typical value would look
@REM similar to:
@REM
@REM    SSH_AUTH_SOCK=/tmp/.ssh-pageant-USERNAME
@REM

@REM Enable extensions, the `verify` call is a trick from the setlocal help
@VERIFY other 2>nul
@SETLOCAL EnableDelayedExpansion
@IF ERRORLEVEL 1 (
    @ECHO Unable to enable extensions
    @GOTO failure
)

@REM Ensure that SSH_AUTH_SOCK is set
@if "x" == "x%SSH_AUTH_SOCK%" @(
    @ECHO The SSH_AUTH_SOCK environment variable must be set prior to running this script. >&2
    @ECHO This is typically configured as a persistent USER variable, using a MSYS2 path for >&2
    @ECHO the ssh-pageant authentication socket as the value. Something similar to: >&2
    @ECHO. >&2
    @ECHO    SSH_AUTH_SOCK=/tmp/.ssh-pageant-%USERNAME% >&2
    @GOTO failure
)

@REM Start ssh-pageant if needed by git
@FOR %%i IN ("git.exe") DO @SET GIT=%%~$PATH:i
@IF EXIST "%GIT%" @(
    @REM Get the ssh-pageant executable
    @FOR %%i IN ("ssh-pageant.exe") DO @SET SSH_PAGEANT=%%~$PATH:i
    @IF NOT EXIST "%SSH_PAGEANT%" @(
        @FOR %%s IN ("%GIT%") DO @SET GIT_DIR=%%~dps
        @FOR %%s IN ("!GIT_DIR!") DO @SET GIT_DIR=!GIT_DIR:~0,-1!
        @FOR %%s IN ("!GIT_DIR!") DO @SET GIT_ROOT=%%~dps
        @FOR %%s IN ("!GIT_ROOT!") DO @SET GIT_ROOT=!GIT_ROOT:~0,-1!
        @FOR /D %%s in ("!GIT_ROOT!\usr\bin\ssh-pageant.exe") DO @SET SSH_PAGEANT=%%~s
        @IF NOT EXIST "!SSH_PAGEANT!" @GOTO ssh-pageant-done
    )
)

@REM Time to make the donuts!
@ECHO Starting ssh-pageant...
@FOR /f "usebackq tokens=1 delims=;" %%o in (`"%SSH_PAGEANT%" -qra %SSH_AUTH_SOCK%`) DO @ECHO %%o

:ssh-pageant-done
:failure
}
}}
@REM Do not use "echo off" to not affect any child calls.

@REM Enable extensions, the `verify` call is a trick from the setlocal help
@VERIFY other 2>nul
@SETLOCAL EnableDelayedExpansion
@IF ERRORLEVEL 1 (
    @ECHO Unable to enable extensions
    @GOTO failure
)

@REM Start the ssh-agent if needed by git
@FOR %%i IN ("git.exe") DO @SET GIT=%%~$PATH:i
@IF EXIST "%GIT%" @(
    @REM Get the ssh-agent executable
    @FOR %%i IN ("ssh-agent.exe") DO @SET SSH_AGENT=%%~$PATH:i
    @IF NOT EXIST "%SSH_AGENT%" @(
        @FOR %%s IN ("%GIT%") DO @SET GIT_DIR=%%~dps
        @FOR %%s IN ("!GIT_DIR!") DO @SET GIT_DIR=!GIT_DIR:~0,-1!
        @FOR %%s IN ("!GIT_DIR!") DO @SET GIT_ROOT=%%~dps
        @FOR %%s IN ("!GIT_ROOT!") DO @SET GIT_ROOT=!GIT_ROOT:~0,-1!
        @FOR /D %%s in ("!GIT_ROOT!\usr\bin\ssh-agent.exe") DO @SET SSH_AGENT=%%~s
        @IF NOT EXIST "!SSH_AGENT!" @GOTO ssh-agent-done
    )
    @REM Get the ssh-add executable
    @FOR %%s IN ("!SSH_AGENT!") DO @SET BIN_DIR=%%~dps
    @FOR %%s in ("!BIN_DIR!") DO @SET BIN_DIR=!BIN_DIR:~0,-1!
    @FOR /D %%s in ("!BIN_DIR!\ssh-add.exe") DO @SET SSH_ADD=%%~s
    @IF NOT EXIST "!SSH_ADD!" @GOTO ssh-agent-done
    @REM Check if the agent is running
    @FOR /f "tokens=1-2" %%a IN ('tasklist /fi "imagename eq ssh-agent.exe"') DO @(
        @ECHO %%b | @FINDSTR /r /c:"[0-9][0-9]*" > NUL
        @IF "!ERRORLEVEL!" == "0" @(
            @SET SSH_AGENT_PID=%%b
        ) else @(
            @REM Unset in the case a user kills the agent while a session is open
            @REM needed to remove the old files and prevent a false message
            @SET SSH_AGENT_PID=
        )
    )
    @REM Connect up the current ssh-agent
    @IF [!SSH_AGENT_PID!] == []  @(
        @ECHO Removing old ssh-agent sockets
        @FOR /d %%d IN (%TEMP%\ssh-??????*) DO @RMDIR /s /q %%d
    ) ELSE  @(
        @ECHO Found ssh-agent at !SSH_AGENT_PID!
        @FOR /d %%d IN (%TEMP%\ssh-??????*) DO @(
            @FOR %%f IN (%%d\agent.*) DO @(
                @SET SSH_AUTH_SOCK=%%f
                @SET SSH_AUTH_SOCK=!SSH_AUTH_SOCK:%TEMP%=/tmp!
                @SET SSH_AUTH_SOCK=!SSH_AUTH_SOCK:\=/!
            )
        )
        @IF NOT [!SSH_AUTH_SOCK!] == [] @(
            @ECHO Found ssh-agent socket at !SSH_AUTH_SOCK!
        ) ELSE (
            @ECHO Failed to find ssh-agent socket
            @SET SSH_AGENT_PID=
        )
    )
    @REM See if we have the key
    @"!SSH_ADD!" -l 1>NUL 2>NUL
    @SET result=!ERRORLEVEL!
    @IF NOT !result! == 0 @(
        @IF !result! == 2 @(
            @ECHO | @SET /p=Starting ssh-agent:
            @FOR /f "tokens=1-2 delims==;" %%a IN ('"!SSH_AGENT!"') DO @(
                @IF NOT [%%b] == [] @SET %%a=%%b
            )
            @ECHO. done
        )
        @"!SSH_ADD!"
        @ECHO.
    )
)

:ssh-agent-done
:failure

@ENDLOCAL & @SET "SSH_AUTH_SOCK=%SSH_AUTH_SOCK%" ^
          & @SET "SSH_AGENT_PID=%SSH_AGENT_PID%"

@ECHO %cmdcmdline% | @FINDSTR /l "\"\"" >NUL
@IF NOT ERRORLEVEL 1 @(
    @CALL cmd %*
)
