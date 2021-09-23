# LM backend API

Project configuration

1. install python3.9.7
2. install virtualenv
3. activate virtualenv

4. install all the requirement from requirement.txt
pip install -r requirement.txt

5. database is mysql
setup db credential in configs/db.py

### Migarate
```bash
$ flask db stamp head
$ flask db migrate
$ flask db upgrade
```
    
### To run the app
1. type python app.py in the cmd
2. All the routes are in the folder routes in the file auth.py
3. Database models in folder models in the file base_model.py
