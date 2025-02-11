# Management commands

## Compiling a playlist and other management commands
You can run management commands, such as dump the database or compile the playlist, by using the management script located in `scripts/manage`.

For instance, to compile a playlist:

`scripts/manage compileplaylist path_to_sound_folder`

## Other important management commands:

- Export experiment data to json: `scripts/manage exportexperiment your_slug`

- Export how often sections have been played: `scripts/manage exportplaycount playlist_id`

- Compile translations into binary .mo file: `scripts/manage compilemessages`

- Create a superuser `scripts/manage createsuperuser` (You will be prompted to enter username, email and password.)

## Update translation strings in .po file:
- `scripts/manage makemessages -l nl` or
- `scripts/manage makemessages --all`
