# yasschat-alx-foundations-portfolio-project
# YassChat - ALX Foundations Portfolio Project

YassChat is a real-time chat application developed as part of the ALX Foundations curriculum. This project showcases fundamental skills in web development, Flask, Socket.IO, and more.

## Features

- Real-time chat between users
- User authentication and session management
- Friendship invitations and acceptance
- Message read status and notifications
- Integration of Flask, Socket.IO, and MySQL database

## Technologies Used

- Flask: A lightweight web application framework in Python
- Socket.IO: Real-time web application framework
- MySQL: Database for storing user information and chat messages
- HTML/CSS: Frontend design and styling
- JavaScript: Client-side scripting for dynamic functionality
- CORS: Cross-Origin Resource Sharing for handling requests from different origins

## How to Run

1. Clone the repository: `git clone https://github.com/yourusername/YassChat.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your MySQL database and update configuration in `config.py`
4. Run the application: `python app.py`
5. Access the application in your web browser: `http://localhost:5000`

## Project Structure

- `/templates`: HTML templates for different views
- `/static`: Static files (CSS, JavaScript, images)
- `/app.py`: Main application file
- `/config.py`: Configuration settings
- `/models.py`: Database models for User, Message, Friendship, etc.
- `/routes.py`: Flask routes for handling HTTP requests
- `/socket_events.py`: Socket.IO events and handlers

## Contributions

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).


