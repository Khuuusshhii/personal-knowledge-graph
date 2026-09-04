@echo off
echo Starting backend...
call env\Scripts\activate
python main.py
echo Starting frontend...
cd frontend
npm start
