# The admin interface

After starting the containers through Docker, you can access Django's admin interface. This is used to create and change playlists, and to set up experiments.

Navigate to [localhost:8000/admin](http://localhost:8000/admin) to see the admin interface.
<img width="941" alt="admin" src="https://github.com/Amsterdam-Music-Lab/MUSCLE/assets/11174072/40aff96c-a336-400b-8a47-4ce04d621a77">

Log in:
- username: admin
- password: admin

(This is set through the .env file. Obviously, these passwords are only suitable for local development!)

You can see an overview of different Django apps:
<img width="656" alt="adminList" src="https://github.com/Amsterdam-Music-Lab/MUSCLE/assets/11174072/877b2850-ce62-4303-bd08-427c3c48bd46">
- **Experiment** to add experiments and experiment series
- **Participant** with information of participants of experiments (automatically created)
- **Section** with information of Playlists and Sections, which may optionally be tied to Songs (i.e., artist and title of a song)
- **Session** with information on experiment sessions (automatically created)
