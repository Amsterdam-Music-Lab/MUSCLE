# The admin interface

After starting the containers through Docker, you can access Django's admin interface. This is used to create and change playlists, and to set up experiments.

Navigate to <a href="http://localhost:8000/admin" target="_blank">localhost:8000/admin</a> to see the admin interface.
<img width="941" alt="admin" src="https://github.com/Amsterdam-Music-Lab/MUSCLE/assets/11174072/40aff96c-a336-400b-8a47-4ce04d621a77">

Log in:
- username: admin
- password: admin

(This is set through the .env file. Obviously, these passwords are only suitable for local development!)

You can see an overview of different Django apps:
<img width="656" alt="adminList" src="/assets/images/admin/AdminInterface.png">

- **Admin_Interface** to customize how this admin interface appears to you
- **Authentication and Authorization** to give other researchers access to this admin interface
- **Experiment** to add experiments and experiment series
- **Image** to add images to be shown as logos or in experiments
- **Participant** with information of participants of experiments (automatically created)
- **Question** to add or edit profile type questions for participants
- **Section** with information of Playlists and Sections, which may optionally be tied to Songs containing artist/title  information
- **Session** with information on experiment sessions (automatically created)
- **Theme** to configure backgrounds, fonts and logos used during an experiment
