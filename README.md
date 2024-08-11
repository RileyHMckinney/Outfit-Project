# Wardrobe Planner
Wardrobe Planner is a web application that allows users to manage their wardrobe by adding
clothing items, creating outfits, and organizing their fashion choices. This project is built with a Flask
backend and a React frontend, providing a seamless and user-friendly interface for wardrobe
management.
## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
## Features
- **User Management**: Create and manage users.
- **Clothing Items**: Add, edit, delete, and view clothing items.
- **Outfit Creation**: Create outfits by selecting combinations of clothing items.
- **Unique Outfit Names**: Ensures that outfit names are unique per user.
- **Responsive Design**: User-friendly interface for managing your wardrobe on any device.
## Installation
To set up this project locally, follow these steps:
### Backend Setup
1. **Clone the Repository:**
 ```bash
 git clone https://github.com/your-username/wardrobe-planner.git
 cd wardrobe-planner
 ```
2. **Create and Activate a Virtual Environment:**
 ```bash
 python -m venv venv
 source venv/bin/activate # On Windows, use `venv\Scriptsctivate`
 ```
3. **Install Backend Dependencies:**
 ```bash
 pip install -r requirements.txt
 ```
4. **Set Up the Database:**
 ```bash
 flask db init
 flask db migrate -m "Initial migration."
 flask db upgrade
 ```
5. **Run the Backend Server:**
 ```bash
 flask run
 ```
### Frontend Setup
1. **Navigate to the Frontend Directory:**
 ```bash
 cd wardrobe-frontend
 ```
2. **Install Frontend Dependencies:**
 ```bash
 npm install
 ```
3. **Run the Frontend Server:**
 ```bash
 npm start
 ```
## Usage
Once the servers are running, you can access the application at `http://localhost:3000`.
### Creating a User
1. Navigate to the home page and create a new user.
2. You can view and manage users from the home page.
### Managing Clothing Items
1. After selecting a user, add clothing items to their wardrobe.
2. You can edit or delete clothing items as needed.
### Creating and Managing Outfits
1. Select clothing items and create unique outfits.
2. Ensure that outfit names are unique for each user.
## API Endpoints
The backend provides a RESTful API with the following endpoints:
- **Users:**
 - `GET /users`: Get all users.
 - `POST /users`: Create a new user.
 - `GET /users/<id>`: Get a specific user by ID.
 - `PUT /users/<id>`: Update a user by ID.
 - `DELETE /users/<id>`: Delete a user by ID.
- **Clothing Items:**
 - `GET /users/<user_id>/clothing_items`: Get all clothing items for a user.
 - `POST /users/<user_id>/clothing_items`: Create a new clothing item for a user.
 - `PUT /users/<user_id>/clothing_items/<item_id>`: Update a clothing item by ID.
 - `DELETE /users/<user_id>/clothing_items/<item_id>`: Delete a clothing item by ID.
- **Outfits:**
 - `GET /users/<user_id>/outfits`: Get all outfits for a user.
 - `POST /outfits`: Create a new outfit.
 - `GET /outfits/<id>`: Get a specific outfit by ID.
 - `PUT /outfits/<id>`: Update an outfit by ID.
 - `DELETE /outfits/<id>`: Delete an outfit by ID.
## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.
## License
This project is licensed under the MIT License. See the LICENSE file for details.
## Contact
If you have any questions or suggestions, feel free to contact me at mckinneyriley13@gmail.com
