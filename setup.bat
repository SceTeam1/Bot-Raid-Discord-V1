@echo off
title Installation des modules Python...
echo.
echo [*] Installation des dépendances necessaire pour le bon fonctionnement...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.
echo [✔] Installation terminée merci de lancer le run.bat.
pause
