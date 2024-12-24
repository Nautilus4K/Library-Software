## Library Software (vi-VN)
  Vietnamese Library software, built with SQLite, Python, HTML, CSS and Javascript. This is a project I made for a try at the scientific and technical competition in Dak Lak Province, Viet Nam.

## Starting the webserver
#### 1. Default HTTPD webserver (Designed for instant port open)

  To start the web server, open the python script `server.py` to run it up. Port 443 is default (for HTTPS connections), change if necessary. To change IP and port on launch as launch arguments, refer to this example of opening webserver on 0.0.0.0 port 443:
  ```bash
  python server.py 0.0.0.0:443
  ```
  **Reminder**: SSL certificate of server is invalid, therefore must be replaced with a functional one before taking this to consumer use or actual test using. Also, this is HTTPD based, so its not a very good choice if you are actually doing something about opening this website online (In that case use the WSGI script).

#### 2. WSGI webserver (Designed for putting on an infrastructure)

  To start the webserver (in Linux distros with the `gunicorn` package preinstalled), open the python script `server_wsgi.py` through gunicorn with this command:
  ```bash
  gunicorn server_wsgi:application
  ```
  **Reminder**: If ran with gunicorn, HTTP**S** connecttion is not necessarily guarranteed to work by default, tinker around with gunicorn to find it, and this will be usable on hosting websites which allow for Python Application and requires WSGI for their web app implementation.

## Change database informations
  To change database informations, open python scripts: `books.py`, `ids.py`, `borrows.py`, `users.py`.

## Enable facial recoginition functionality
### Registering a face
  To register a face, you can open up `face_reg.py` to register and test check your face using its 2 functionalities.
### Enable facial recoginition login
  To enable functional facial recoginition on login page, open `face_server.py`, it will automatically enable facial recoginition functionality.
### Modify similarity threshold
  In `face_server.py`, you can edit how similar one person can be from the other, purely for security reasons to make sure that one's face cannot be mistaken for another person. To edit, go to `face_server.py` and find a variable called `similarity_threshold` inside of the `check_face()` function, here are some examples of this threshold:
  - `1.0`: Very vulnerable. Completely unrelated people can be mistaken for another
  - `0.8`: Moderate vulnerable. Only people which has some kind of similarity in face structure could be mistaken
  - `0.6`: Moderately strict. Only people who really have some similarity in face structure and actually are related (Not sure?) can be mistaken.
  - `0.4`: Actually strict. This requires a good lighting, actual very close similarity between face structures
  - `0.2`: Don't ever use this. Only actual picture copypasters can be mistaken for another person because at that point, they could just strap a picture of the user they want to access into the camera and the AI will make a mistake as it cannot tell the difference between the picture and the actual face of the user, nor the distance of the object facing the camera.
  - `0.0`: Why are you like this? Do you want to be funny? Because I hope not.
---
### The rest is your control. This is open source, feel free to distribute, just remember to credit me.
### Library server software designed for the scientific and technical competition in Buon Ma Thuot City, Dak Lak Province, Vietnam. Made by Nguyen Van Quang Vinh in 2024.
