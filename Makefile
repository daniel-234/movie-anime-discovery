.PHONY: runserver data tailwind


help:
	@echo "Available commands:"
	@echo "  make rs             - Run server"
	@echo "  make data           - Run API data fetching"
	@echo "  make services       - Get the list of service providers from TMDB and create or update it in DB"
	@echo "  make tailwind       - Run development server with Tailwind live update"
	
rs:
	uv run manage.py runserver

data:
	uv run manage.py api_caching

services:
	uv run manage.py sync_services

tailwind:
	uv run manage.py tailwind dev