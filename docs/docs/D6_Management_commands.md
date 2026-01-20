# Management commands

## Compiling a playlist and other management commands
You can run management commands, such as dump the database or compile the playlist, by using the management scripts located in `scripts/manage`. These can be useful to run some MUSCLE-specific tasks as the following:

- to compile a playlist:

`scripts/manage compileplaylist path_to_sound_folder`

- to export block data to json:

`scripts/manage exportblock block_slug`

## Important Django management commands:
- Update translation strings in .po file: - `scripts/manage makemessages -l nl` or `python manage.py makemessages --all`
- Compile translations into binary .mo file: `scripts/manage compilemessages`
- Create a superuser: `scripts/manage createsuperuser` (You will be prompted to enter username, email and password.)

