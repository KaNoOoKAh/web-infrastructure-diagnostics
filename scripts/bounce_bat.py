@echo off
setlocal EnableDelayedExpansion
title Batch Physics Sandbox

:: Window Setup
mode con: cols=60 lines=25
cls

:: Initial Physics States
set "x=30"
set "y=5"
set "vx=1"
set "vy=0"
set "gravity=1"
set "restitution=1"
set "width=58"
set "height=20"

:: Clear Screen Buffer
:init_canvas
for /l %%r in (0,1,%height%) do (
    set "line_%%r="
    for /l %%c in (0,1,%width%) do set "line_%%r=!line_%%r! "
)

:main_loop
:: 1. Clear Ball from Old Position
set "line_!y!=!line_%y%:~0,%x%! !line_%y%:~%x%+1!"

:: 2. Apply Gravity & Update Velocity/Position
set /a "vy+=gravity"
set /a "x+=vx"
set /a "y+=vy"

:: 3. Wall Collisions (Left / Right)
if !x! GEQ %width% (
    set "x=%width%"
    set /a "vx=-vx"
)
if !x! LEQ 0 (
    set "x=0"
    set /a "vx=-vx"
)

:: 4. Floor / Ceiling Collisions
if !y! GEQ %height% (
    set "y=%height%"
    set /a "vy=-vy"
    :: Dampen velocity slightly on floor bounce
    set /a "vy=vy + 1"
)
if !y! LEQ 0 (
    set "y=0"
    set /a "vy=-vy"
)

:: 5. Draw Ball at New Position
set "line_!y!=!line_%y%:~0,%x%!O!line_%y%:~%x%+1!"

:: 6. Render Frame to Terminal
cls
for /l %%r in (0,1,%height%) do echo !line_%%r!
echo ============================================================
echo  Position: (!x!, !y!)  ^|  Velocity: (!vx!, !vy!)

:: Frame Delay
for /l %%i in (1,1,1500) do rem

goto main_loop
