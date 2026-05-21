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

For local development, set `DATABASE_URL=sqlite:///db.sqlite3` — the database file will be created in the project root the first time you run migrations.

### Requirements

This project is built with the Django framework and it uses the ```django-tailwind``` package to apply Tailwind CSS for styling. As some dependencies are needed to make it work and they require Node.js to work in development mode, you need to install them in the project local environment:
```
cd theme/static_src && npm install
```
Then, navigate back to the project root.
```
cd -
```

### Generate the migration files

To create the database tables based on the models defined, Django needs to sync the migration files. 
```
uv run manage.py migrate
```

### Populate the Database

To populate the database, call the API fetching command. 
```
make data
```

### Get the service providers available in TMDB

To show the services availability in detail pages, it is necessary to run the command to fetch the data
from the TMDB API.
```
make services
```

## Run the app

Run the command: 
``` 
make tailwind
``` 
and then navigate to http://127.0.0.1:8000/ to see the app running. 

## Deployment

The app is deployed on [Fly.io](https://fly.io/) using SQLite on a persistent volume. Migrations run automatically on container startup via the Dockerfile `CMD`.

To deploy changes:
```
fly deploy
```

To inspect or interact with the production database:
```
fly ssh console -C "python manage.py shell"
```

To run management commands in production (e.g. data refresh):
```
fly ssh console -C "python manage.py api_caching"
fly ssh console -C "python manage.py sync_services"
```