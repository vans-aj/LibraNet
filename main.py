# main.py (if using the traditional method)

from app import create_app

# The app instance is created as before
app = create_app()

# This block is what you are asking about
port = 8080
if __name__ == '__main__':
    # This runs the app using Flask's simpler, built-in server
    app.run(port=port,debug=True)