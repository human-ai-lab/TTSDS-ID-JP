@echo off
python initialize.py "false"
if errorlevel 1 (
    echo Error occurred during download!
    pause
) else (
    echo Download completed successfully!
)
pause

