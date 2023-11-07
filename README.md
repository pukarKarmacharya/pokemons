Backend of Serving list of pokemons
This API has 2 route
1) Get route
This route is responsible for filtering pokemon by name, type and list of all pokemon
2) Users route
This route is responsible for creating users and searching user by id
How to run locally
First clone this repo by using following command
git clone https://github.com/pukarKarmacharya/pokemons.git
then
cd pokemons
Then install fastapi using all flag:
pip install fastapi[all]
Then go to this repo folder in your local computer and run following command
uvicorn app.main:app --reload
Then you can use following link to use the API
http://127.0.0.1:8000/docs 
After run this API you need a database in postgres
Create a database in postgres then create a file name .env and write the following things in you file
DATABASE_HOSTNAME = localhost
DATABASE_PORT = 5432
DATABASE_PASSWORD = passward_that_you_set
DATABASE_NAME = name_of_database
DATABASE_USERNAME = User_name
