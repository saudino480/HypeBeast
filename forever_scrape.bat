call C:\Users\Olympus\Anaconda3\Scripts\activate.bat C:\Users\Olympus\Anaconda3

SET /A "index = 5"
SET /A "count = 0"
:while
if %index% geq %count% (
   python grailed_scrapper.py
   SET /A "index = index + 1"
   goto :while
)
