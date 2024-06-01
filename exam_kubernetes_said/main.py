from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text

# Création d'un serveur FastAPI
server = FastAPI(title='User API')

# Création d'une connexion à la base de données
mysql_url = '127.0.0.1:3306'  
mysql_user = 'root'
mysql_password = "datascientest1234"  # mot de passe de la base de données MySQL
database_name = 'Main'

# recreating the URL connection
connection_url = 'mysql://{user}:{password}@{url}/{database}'.format(
    user = mysql_user,
    password = mysql_password,
    url = mysql_url,
    database = database_name
)

# creating the connection
mysql_engine = create_engine(connection_url)


# creating a User class
class User(BaseModel):
    user_id: int = 0
    username: str = 'daniel'
    email: str = 'daniel@datascientest.com'

@server.get('/status')
async def get_status():
    """Retourne 1"""
    return 1

@server.get('/users')
async def get_users():
    with mysql_engine.connect() as connection:
        results = connection.execute(text('SELECT * FROM Users;'))

    results = [
        User(
            user_id=i[0],
            username=i[1],
            email=i[2]
        ) for i in results.fetchall()]
    return results

@server.get('/users/{user_id:int}', response_model=User)
async def get_user(user_id):
    with mysql_engine.connect() as connection:
        results = connection.execute(text('SELECT * FROM Users WHERE Users.id = {};'.format(user_id)))
            

    results = [
        User(
            user_id=i[0],
            username=i[1],
            email=i[2]
            ) for i in results.fetchall()]

    if len(results) == 0:
        raise HTTPException(
            status_code=404,
            detail='Unknown User ID')
    else:
        return results[0]

