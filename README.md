# Movie and Anime Discovery Platform

A discovery platform to tag your favourite movies, anime and manga or to track what are currently the trending titles, as reported in specialized websites like TMDB or AniList. 

## Setup

```
git clone https://github.com/daniel-234/movie-anime-discovery.git
cd movie-anime-discovery
uv sync
```

### Environment variables

You need to create some environemnt variables as defined in ```.env-template```.
Create a ```.env``` file in the root of your project and provide all the values required in the template file. 

### Requirements

This project is built with the Python framework Django and it uses the ```django-tailwind``` package to apply Tailwind CSS for styling. As some dependencies are needed to make it work and they  require Node.js to work in development mode, you need to install Node and other files in the project local environment:
```
cd theme/static_src && npm install
```
Then, navigate back to the project root.
```
cd movie-anime-dicovery
```

### Generate the migration files

To create the database tables based on the models defined, Django needs to generate the migration files based on the models and then apply them to the database. 
```
uv run manage.py makemigrations
uv run manage.py migrate
```

### Populate the Database

To populate the database, call the API fetching command. 
```
make data
```

## Run the app

Run the command: 
``` 
make tailwind
``` 
and then navigate to http://127.0.0.1:8000/ to see the app running. 