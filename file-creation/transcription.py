import os
from prompt_toolkit import prompt
from datetime import date

print("lfg!")
name = prompt("name of song: ")
mod_name = "-".join(name.split())

instrument = prompt("instrument being transcribed: ")
mod_instrument = "-".join(instrument.split())

date_of_transcription = date.today().isoformat()

folder_name = f"{date_of_transcription}-{mod_name}-{mod_instrument}"

path = "/Users/ananyageorge/Documents/projects/battle-stations/music/transcription/"
final_path = os.path.join(path, folder_name)

try:
    os.mkdir(final_path)
except OSError as _:
    print("file already exists")

os.system(f"cd {final_path} && nvim notes.txt")
