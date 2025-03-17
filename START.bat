@echo off
:loop
python update_config.py
timeout /t 10
python translate.py
timeout /t 150
goto loop
