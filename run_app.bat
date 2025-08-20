@echo off
python -m streamlit run app.py
if errorlevel 1 (
    echo Streamlit crashed! Check for errors.
    pause
)
cmd /k
