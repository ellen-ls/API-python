# Pokémon Teams Management App

This is a web application built with Flask that allows users to create and manage Pokémon teams. Users can register their teams, add Pokémon to their teams, and view all registered teams.

## Features:

- Create new Pokémon teams

- Add Pokémon to existing teams

- View all registered Pokémon teams

- Error handling for invalid Pokémon names and missing user input

## Endpoints:

- GET /: Renders the HTML interface for creating and viewing Pokémon teams.

- GET /api/teams: Retrieves all registered teams.

- GET /api/teams/{username}: Retrieves a team by username.

- POST /api/teams: Creates a new team or adds Pokémon to an existing team.

## Installation:

 ``` 
 pip install -r requirements.txt
```

## Usage:

1. Run the Flask application:   
  ```` python app.py ````

 2. Open your web browser and go to http://localhost:5000 to access the application.

 3. To create or update a Pokémon team, use the provided form on the homepage. Enter your username and select Pokémon from the dropdown menu. Click "Create Team" to submit.

 4. To view all registered teams, navigate to http://localhost:5000/api/teams in your browser.

 5. To search for teams by user, use the endpoint `http://localhost:5000/api/teams/<username>`, replacing `<username>` with the desired username.

## Docker

Alternatively, you can run the application using Docker.

1. Build the Docker image:
   ``` 
   docker build -t pokemon-api.
   ```

3. Run the Docker container:
   ```
   docker run --rm -p 5000:5000 pokemon-api
   ```

5. Access the application at http://localhost:5000 as described above.

## Contributing

Contributions are welcome! Please feel free to submit bug reports, feature requests, or pull requests.


   

   

