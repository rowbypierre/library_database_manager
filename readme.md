# Project Title
Library Database Manager

# Description
This project provides an interactive Python script that enables end users to perform CRUD (Create, Read, Update, Delete) operations on a Library Postgres database through the terminal. It is designed to facilitate database interactions without requiring direct SQL query knowledge from the user. The script makes use of several Python files to manage database connections, user authentication, and CRUD operations in an intuitive manner.

## Key Components

### `config.py`
- **Purpose:** Stores configuration details for the database connection, including database name, user credentials, and host information.
- **Contents:** Contains variables defining the database name, user, password, and host. This file is essential for establishing a secure connection to the Postgres database.

### `connect.py`
- **Purpose:** Establishes a connection to the Library Postgres database using parameters defined in `config.py`. It also handles connection errors gracefully.
- **Contents:** Implements a function that utilizes `psycopg2` to connect to the database. It imports configurations from `config.py` and includes error handling for connection issues.

### `login.py`
- **Purpose:** Manages user authentication for the interactive script. It ensures that only authorized users can perform operations on the database.
- **Contents:** Contains logic for user login, including password verification. It may interact with a users table in the database or a pre-defined list of credentials.

### `library_database_manager.py`
- **Purpose:** The core script that provides an interactive interface for performing CRUD operations on the Library database. It allows users to insert, read, update, and delete records from various tables without direct SQL command input.
- **Contents:** 
  - **Interactive Menu:** Offers a user-friendly menu for selecting the desired operation (Create, Read, Update, Delete).
  - **CRUD Operations:** Functions for each CRUD operation, utilizing SQL commands executed through `psycopg2`. These functions are designed to be intuitive and guide the user through the required steps for each operation.
  - **Input Validation:** Ensures that user inputs are validated before executing database operations to maintain data integrity.
  - **Error Handling:** Robust error handling mechanisms to provide clear feedback to the user in case of invalid inputs or database errors.

## How to Use
Here's a simple and concise guide on how to use the interactive Python script for managing library database records:

1. **Start the Program**: Run the script from your terminal. The program will prompt you to log in.

2. **Log In**:
   - **Username**: You will first be asked to enter your username. Type it in and press Enter.
   - **Password**: Next, you'll be prompted for your password. Type it in carefully (it won't be visible for security reasons) and press Enter.

3. **Main Menu**: Once logged in, you'll see the main menu with options to Insert, Read, Update, or Delete records in the library database.

4. **Choose an Option**:
   - To **Insert** a new record, follow the prompts to enter the necessary information about a book or member.
   - To **Read** or view records, select the read option, and follow prompts to specify what information you want to view.
   - To **Update** a record, choose the update option, then follow the prompts to select a record and enter the new details.
   - To **Delete** a record, select the delete option, then follow the instructions to specify which record you wish to remove.

5. **Follow Prompts**: For each action you select, the program will guide you through the process with prompts. Simply follow these instructions.

6. **Log Out/Exit**: Once you've completed your tasks, you can exit the program or log out as directed by the on-screen instructions.

Remember, you don't need any knowledge of SQL or database management to use this script; just follow the on-screen prompts to manage the library database records effectively.

## Dependencies
To run this project, you'll need to install some external libraries and use built-in Python modules. Here's what you need:

1. **psycopg2**: Connects the script to the PostgreSQL database.
2. **getpass**: Hides your password input for security.

The rest (`sys`, `os`, `time`, `datetime`) are part of Python's standard library, so you don't need to install them separately. Make sure `psycopg2` is installed with `pip install psycopg2` or `pip install psycopg2-binary`.

## Security and Authentication
The project's security is managed through a login system where users must input their username and password. These inputs are checked against preset credentials. Users get multiple tries to enter their details correctly, with a limit of 10 attempts for usernames and 10 for passwords. Exceeding these attempts leads to the program shutting down, ensuring access is restricted to authorized users and guarding against unauthorized access attempts.

## Contributing
To contribute to this project, please follow these steps: 

1. Fork the project repository to your own account.
2. Make your changes or additions in your forked version.
3. Submit a pull request with a clear description of your updates or enhancements.
4. Wait for the project maintainers to review and merge your contributions.

For detailed instructions or specific contribution guidelines, refer to the project's documentation or contact the maintainers.