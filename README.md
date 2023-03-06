# Transaction Queue API

## Project Setup

- Create and activate your virtual environment
- In the root folder, run `pip install -r requirements.txt` to install the required libraries.
- Create a ".env" file in the root fold.
- The sample content of the ".env" file can be found in the ".env.sample" file also in the root folder.

### Database tables creation

- Change into `/src` folder.
- Run `alembic updgrade head` to create the neccessary database tables.

## Start Development Server

- Change into `/src` folder
- Run `python main.py` to start the development server.
- By default, your application will be running on port 8000.
