import os
import datetime


today = datetime.date.today()
filepath = "/Users/ananyageorge/Dropbox/Captain's Log/"

os.chdir(filepath)
os.system(f"nvim {today}.txt")
