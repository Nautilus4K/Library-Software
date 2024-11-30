## Library Software (vi-VN)
  Vietnamese Library software, built with SQLite, Python, HTML, CSS and Javascript. This is a project I made for a try at the scientific and technical competition in Dak Lak Province, Viet Nam.

## Starting the webserver
  To start the web server, open the python script `server.py` to run it up. Port 443 is default (for HTTPS connections), change if necessary. To change IP and port on launch as launch arguments, refer to this example of opening webserver on 0.0.0.0 port 443:
  ```bash
  python server.py 0.0.0.0:443
  ```
  **Reminder**: SSL certificate of server is invalid, therefore must be replaced with a functional one before taking this to consumer use or actual test using.

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
  - `0.2`: Don't ever use this. Only actual 

---
---
### The rest is your control. This is open source, feel free to distribute, just remember to credit me.
