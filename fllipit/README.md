# FLLiPit
A simple pit display for use at Maine FIRST Lego League Events.
Gathers data from a Microsoft Access database, then publishes rankings and palyoff progression to webpage using Python Flask package.

### Using the Application:
Install Python 3.x: https://www.python.org/downloads/

Install pip: https://pip.pypa.io/en/latest/installing.html

Install virtualenv
```text
> pip install virtualenv
```

Clone the repository
```text
> git clone https://github.com/rtfoley/fllipit.git
```

Create and activate a virtual environment and install dependencies
```text
> cd fllipit
> virtualenv venv
> .\\venv\Scripts\activate
```

Use Pip to install dependencies
```text
(venv) > pip install -r requirements.txt
```

Set the 'Event Name' and 'DB File' properties in config.py
```python
EVENT_NAME = 'Maine FLL Championship'
DB_FILE = 'C:\\path\\to\\access\\database.accdb'
```

Run the application
```text
(venv) > python fllipit.py
```

The rankings page will be available at http://localhost:5000

The playoff ladder will be available at http://localhost:5000/ladder

#### Using the temporary database (development)
This is useful for developing the application on systems that don't have MS Access installed.

Follow the directions above, through the dependency installation.

Set the 'Test DB' property in config.py to True
```python
TEST_DB = True
```

Create the database (only if using test database instead of an actual MS Access database)
```text
(venv)$ python create_db.py
```

Run the application
```text
$ python fllipit.py
```
