@echo off

REM Create README.md file and write initial content
echo # Overview of FAIR implementation communities and profiles > README.md
echo This repository gives a daily update of available FAIR implementation communities, profiles and the respective answers to I2 data and I3 metadata. >> README.md
echo. >> README.md

REM Execute the Python script and append the output to README.md
python run2.py >> README.md
