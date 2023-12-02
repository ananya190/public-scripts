keybind helper

- store the command and its shortcut in the following form
  command : shortcut
- possibly use json files
- different files for different programs
- store one for aliases too (keep each file short)
- when the program is called, it presents a prompt with a fuzzy completer with the different file names
- cowsay the shortcuts
- inspiration from the telescope cowsay picture in this folder


setup
=====

create a keys folder here and symlink to ~/.local/share -- this is the data
create a keys script and symlink to ~/.local/bin/ -- this is the script

notes
=====

cowsay has a fixed width and doesn't work quite as well as i'd like it to
