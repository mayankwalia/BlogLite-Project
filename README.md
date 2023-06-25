# BlogLite-app
- Project submitted by **Mayank Walia** 21f1004343.
- A BlogLite web app as part of the IITM POD MAD-1 Diploma Project. It allows the user to create and edit their blogs by attaching the images. Users can follow and unfollow others, like and comment on different blogs. Each user has its own profile page and a personalized feed based on his following. Users can find new connections by searching using their usernames.

# Local Setup
- Create virtual environment. On VS Code terminal execute `python -m venv env`
- Activate virtual environment. On VS Code terminal execute `.\env\Scripts\Activate.ps1` 
- Run `pip install -r requirements.txt` to install all dependencies
- Install other dependencies in case not present on your system

# Local Development Run
- `python -m app.py` It will start the flask app in `development`. Suited for local development. 


# Accessing API

- Refer to the YAML file for making API requests to retrive data.

# Demo link
- A demostration of how the app was made and is to be used is provided [here](https://drive.google.com/file/d/1lbaT7bqmBP84ZWX_cp1HP-SGOERkFr1r/view?usp=share_link)

# Folder Structure

- `testdb.db` is the sqlite DB. 
- `/` is where our application code is
- `static` - default `static` files folder. It serves at '/static' path.
- `templates` - Default flask templates folder

# Directory Tree
```
.
├── Project Report.pdf
├── README.md
├── api.py
├── app.py
├── application
│   ├── __init__.py
│   ├── models.py
│   ├── posts
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── posts_views.py
│   ├── static
│   │   ├── bootstrap
│   │   │   ├── css
│   │   │   │   ├── bootstrap-grid.css
│   │   │   │   ├── bootstrap-grid.css.map
│   │   │   │   ├── bootstrap-grid.min.css
│   │   │   │   ├── bootstrap-grid.min.css.map
│   │   │   │   ├── bootstrap-grid.rtl.css
│   │   │   │   ├── bootstrap-grid.rtl.css.map
│   │   │   │   ├── bootstrap-grid.rtl.min.css
│   │   │   │   ├── bootstrap-grid.rtl.min.css.map
│   │   │   │   ├── bootstrap-icons.css
│   │   │   │   ├── bootstrap-reboot.css
│   │   │   │   ├── bootstrap-reboot.css.map
│   │   │   │   ├── bootstrap-reboot.min.css
│   │   │   │   ├── bootstrap-reboot.min.css.map
│   │   │   │   ├── bootstrap-reboot.rtl.css
│   │   │   │   ├── bootstrap-reboot.rtl.css.map
│   │   │   │   ├── bootstrap-reboot.rtl.min.css
│   │   │   │   ├── bootstrap-reboot.rtl.min.css.map
│   │   │   │   ├── bootstrap-utilities.css
│   │   │   │   ├── bootstrap-utilities.css.map
│   │   │   │   ├── bootstrap-utilities.min.css
│   │   │   │   ├── bootstrap-utilities.min.css.map
│   │   │   │   ├── bootstrap-utilities.rtl.css
│   │   │   │   ├── bootstrap-utilities.rtl.css.map
│   │   │   │   ├── bootstrap-utilities.rtl.min.css
│   │   │   │   ├── bootstrap-utilities.rtl.min.css.map
│   │   │   │   ├── bootstrap.css
│   │   │   │   ├── bootstrap.css.map
│   │   │   │   ├── bootstrap.min.css
│   │   │   │   ├── bootstrap.min.css.map
│   │   │   │   ├── bootstrap.rtl.css
│   │   │   │   ├── bootstrap.rtl.css.map
│   │   │   │   ├── bootstrap.rtl.min.css
│   │   │   │   └── bootstrap.rtl.min.css.map
│   │   │   └── js
│   │   │       ├── bootstrap.bundle.js
│   │   │       ├── bootstrap.bundle.js.map
│   │   │       ├── bootstrap.bundle.min.js
│   │   │       ├── bootstrap.bundle.min.js.map
│   │   │       ├── bootstrap.esm.js
│   │   │       ├── bootstrap.esm.js.map
│   │   │       ├── bootstrap.esm.min.js
│   │   │       ├── bootstrap.esm.min.js.map
│   │   │       ├── bootstrap.js
│   │   │       ├── bootstrap.js.map
│   │   │       ├── bootstrap.min.js
│   │   │       └── bootstrap.min.js.map
│   │   ├── carousel
│   │   │   ├── comment.JPG
│   │   │   ├── create.JPG
│   │   │   ├── feed.JPG
│   │   │   ├── profile.JPG
│   │   │   └── search.JPG
│   │   ├── customStyles.css
│   │   ├── engagement_data
│   │   ├── favicon.ico
│   │   └── images
│   │       ├── default_blogpost.png
│   │       └── default_profile.jpg
│   ├── templates
│   │   ├── 404.html
│   │   ├── 500.html
│   │   ├── base.html
│   │   ├── comment.html
│   │   ├── create_or_update_post.html
│   │   ├── dashboard.html
│   │   ├── feed.html
│   │   ├── home.html
│   │   ├── insights.html
│   │   ├── login.html
│   │   ├── macros
│   │   │   ├── fields.html
│   │   │   └── imagefield.html
│   │   ├── posts.html
│   │   ├── search_users.html
│   │   ├── serach_results.html
│   │   ├── signup.html
│   │   ├── template.html
│   │   ├── update_password.html
│   │   ├── update_profile.html
│   │   └── userposts.html
│   ├── users
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── views.py
│   └── utility.py
├── bloglite_api.yaml
├── configuration.py
└── requirements.txt

12 directories, 90 files
```