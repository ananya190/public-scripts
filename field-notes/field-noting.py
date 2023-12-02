import os
import datetime

today = datetime.date.today()

filepath = "/Users/ananyageorge/Documents/field-notes/"
os.chdir(filepath)
os.system(f"nvim {today}.txt")
