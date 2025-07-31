import mysql.connector
import re
from datetime import datetime
from abc import abstractmethod
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from tabulate import tabulate
from fpdf import FPDF
from colorama import init, Fore, Style

init(autoreset=True)

class DatabaseConnection:

    def __init__(self, host, user, password, database):
            self.host = host
            self.user = user
            self.password = password
            self.database = database
            self.conn = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            # print("Connection successful!")
            return True
        except mysql.connector.Error as e:
            # print(f"Error: {e}")
            print(Fore.RED + "Password is incorrect")
            return False
        
    def close(self):
        try:
            
            if self.conn is not None and self.conn.is_connected():
                self.conn.close()  # ✅ Then close the connection
                self.conn = None
                print(Fore.WHITE + "Database connection closed.")

        except Exception as e:
            print(Fore.RED + f"Error closing database connection: {e}")

class MovieCollection:
    
    def __init__(self):
        self.movies = {}
        self.actors = {}
        self.directors = {}
        self.users = {}
        self.db = DatabaseConnection("localhost", "root", self.get_password(), "movie")
        
        if self.db.connect():
            self.cursor = self.db.conn.cursor()
            self.load_movies()
            self.load_directors()
            # self.load_customers()
            # self.load_user()
            self.load_actors()
            self.load_users()
            print("Main menu is shown.")
        else:
            print("Exiting the program.")
            exit()
        self.cursor = self.db.conn.cursor()
        
    def get_password(self):
        password = input(Fore.GREEN + "Enter password: ")
        return password
        
    def load_movies(self):
        """Load movies from the database into the in-memory movies dictionary."""
        try:
            # Use the cursor initialized in the Movie class
            self.cursor.execute("SELECT * FROM Movies")
            movies = self.cursor.fetchall()

            # Populate the in-memory movies dictionary
            self.movies = {
                movie[0]: {
                    "movie_name": movie[1],
                    "duration": movie[2],
                    "released_year": movie[3],
                    "genre": movie[4]
                }
                for movie in movies
            }

            # print("Movies loaded successfully into memory.")
            if self.movies:
                pass
            else:
                print(Fore.RED + "No movies found in the database.")
        except Exception as e:
            print(Fore.RED + f"Error loading movies: {e}")

    def load_actors(self):
        """Load actors from the database into the in-memory actors dictionary."""
        try:
            self.cursor.execute("SELECT * FROM Actors")
            actors = self.cursor.fetchall()
            
            # Populate the in-memory actors dictionary
            self.actors = {
                actor[0]: {
                    "name": actor[1],
                    "birth_date": actor[2],
                    "gender": actor[3],
                    # "movies": actor[4]  # Assuming this is a comma-separated list of movie IDs
                }
                for actor in actors
            }
            
            # print(Fore.WHITE + "Actors loaded successfully into memory.")
            if not self.actors :
                print(Fore.RED + "No actors found in the database.")
        except Exception as e:
            print(Fore.RED + f"Error loading actors: {e}")

    def load_directors(self):
        """Load directors from the database into the in-memory self.directors dictionary."""
        try:
            # Query the database to fetch all directors
            self.cursor.execute("SELECT director_id, director_name, birth_date, gender FROM Directors")
            directors = self.cursor.fetchall()
            
            # Populate the in-memory directors dictionary
            self.directors = {
                director[0]: {
                    "director_name": director[1],
                    "birth_date": director[2],
                    "gender": director[3]
                }
                for director in directors
            }
            
            # print(Fore.WHITE + "Directors loaded successfully into memory.")
            
            # Display directors
            if self.directors:
                # for director_id, director_data in self.directors.items():
                #     print(f"Director ID: {director_id}, Name: {director_data['director_name']}, "
                #         f"Birth Date: {director_data['birth_date']}, Gender: {director_data['gender']}")
                pass
            
            else:
                print(Fore.RED + "No directors found in the database.")
        
        except Exception as e:
            print(Fore.RED + f"Error loading directors: {e}")
            
    def load_users(self):
        """Load users from the database into the in-memory users dictionary."""
        try:
            # Use the cursor initialized in the class
            self.cursor.execute("SELECT * FROM Users")
            users = self.cursor.fetchall()

            # Populate the in-memory users dictionary
            self.users = {
                user[0]: {
                    "user_name": user[1],
                    "user_email": user[2],
                    "password": user[3]
                }
                for user in users
            }

            # print(Fore.WHITE + "Users loaded successfully into memory.")
            if not self.users:
                print(Fore.RED + "No users found in the database.")
        except Exception as e:
            print(Fore.RED + f"Error loading users: {e}")



    def get_password(self):
        password = input(Fore.GREEN + "Enter password: ")
        return password
    
    def isValid_email(self):
        while True:
            try:
                email = input(Fore.GREEN + "Enter email: ")
                # Validate email format
                email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_regex, email):
                    print(Fore.RED + "Invalid email format. Please enter a valid email address.")
                    continue
                
                else:
                    return email
            except Exception as e:
                print(Fore.RED + f"Error validating email: {e}")
        
    def isValid_mobile_number(self):
        while True:
            try:
                mobile_number = input(Fore.GREEN + "Enter mobile number: ")
                # Validate mobile number format (e.g., 10 digits, optional country code)
                mobile_regex = r'^\+?\d{10,15}$'
                if not re.match(mobile_regex, mobile_number):
                    print(Fore.RED + "Invalid mobile number format. Please enter a valid mobile number.")
                    continue
                else:
                    return mobile_number
            except Exception as e:
                print(Fore.RED + f"Error validating mobile number: {e}")

    def get_valid_date(self,add,date=None):
        while True:
            if date:
                date_str=date
            else:
                date_str = input(Fore.GREEN + f"Enter {add}birth date (YYYY-MM-DD): ")
            try:
                # Try parsing the date with the format YYYY-MM-DD
                valid_date = datetime.strptime(date_str, "%Y-%m-%d")
                return valid_date.date()  # Return the date part (YYYY-MM-DD)
            except ValueError:
                # If the input doesn't match the format, ask again
                print(Fore.RED + "Invalid date format. Please enter the date in YYYY-MM-DD format.")
                
    # Add code to manage movies here
    @abstractmethod
    def manage_actors(self):
        pass
    
    @abstractmethod
    def manage_movies(self):
        pass
            
    @abstractmethod
    def manage_directors(self):
        pass
    
    def display_menu(self, menu_name, options):
        print(Fore.BLUE + f"{menu_name} Menu:")
        for i, option in enumerate(options, 1):
            print(Fore.YELLOW + f"{i}. {option}")
        
    def get_user_choice(self, options):
        while True:
            try:
                choice = int(input(Fore.GREEN + "Enter your choice: "))
                if 1 <= choice <= len(options):
                    return choice
                else:
                    print(Fore.RED + "Invalid choice, please try again.")
            except ValueError:
                print(Fore.RED + "Invalid input, please enter a number.")

    
    def add_user_rating_to_movie(self):
        """Allows a user to rate a movie after verifying both the user and the movie exist in the database."""
        try:
            # Step 1: Check if users exist
            if not self.users:
                print(Fore.RED + "No users found. Please add a user first.")
                return

            # Step 2: Take user name and check if they exist
            user_name = input("Enter your username: ").strip()

            user_id = None
            for uid, user_info in self.users.items():
                if user_info["user_name"].lower() == user_name.lower():
                    user_id = uid
                    break

            if user_id is None:
                print(Fore.RED + f"User '{user_name}' does not exist.")
                return

            # Step 3: Check if movies exist
            if not self.movies:
                print(Fore.RED + "No movies found. Please add a movie first.")
                return

            while True:
                # Step 4: Take movie name
                movie_name = input("\nEnter the movie name you want to rate (or type 'back' to exit): ").strip()

                if movie_name.lower() == "back":
                    print("Returning to the main menu...")
                    return  # Exit the loop and return

                # Step 5: Check if movie exists
                movie_id = None
                for mid, movie_info in self.movies.items():
                    if movie_info["movie_name"].lower() == movie_name.lower():
                        movie_id = mid
                        break

                if movie_id is None:
                    print(Fore.RED + f"Movie '{movie_name}' does not exist.")
                    continue
                    
                while True:
                    try:
                        rating = float(input("Enter your rating (1-10): ").strip())

                        if 1 <= rating <= 10:
                            break
                        else:
                            print(Fore.RED + "Invalid rating. Please enter a number between 1 and 10.")
                    except ValueError:
                        print(Fore.RED + "Invalid input. Please enter a numeric value between 1 and 10.")

                # Step 7: Insert rating into the User_Ratings table
                query = "INSERT INTO User_Rating (user_id, movie_id, rating) VALUES (%s, %s, %s)"
                self.cursor.execute(query, (user_id, movie_id, rating))
                self.db.conn.commit()

                print(Fore.WHITE + f"User '{user_name}' successfully rated movie '{movie_name}' with a score of {rating}/10.")

        except Exception as e:
            print(Fore.RED + f"Error adding user rating to movie: {e}")
            
            
    def add_actor_to_movie(self):
        """Adds an actor to one or multiple movies after verifying their existence in the database."""
        try:
            # Step 1: Check if actors exist
            if not self.actors:
                print(Fore.RED + "No actors found.")
                return

            # Step 2: Take actor name and check if they exist
            actor_name = input("Enter the actor's name: ").strip()

            actor_id = None
            for aid, actor_info in self.actors.items():
                if actor_info["name"].lower() == actor_name.lower():
                    actor_id = aid
                    break

            if actor_id is None:
                print(Fore.RED + f"Actor '{actor_name}' does not exist.")
                return

            # Step 3: Check if movies exist
            if not self.movies:
                print(Fore.RED + "No movies found. Please add a movie first.")
                return

            while True:
                # Step 4: Take movie name
                movie_name = input("\nEnter the movie name (or type 'back' to exit): ").strip()

                if movie_name.lower() == "back":
                    print("Returning to the main menu...")
                    return  # Exit the loop and return

                # Step 5: Check if movie exists
                movie_id = None
                for mid, movie_info in self.movies.items():
                    if movie_info["movie_name"].lower() == movie_name.lower():
                        movie_id = mid
                        break

                if movie_id is None:
                    print(Fore.RED + f"Movie '{movie_name}' does not exist.")
                    add_movie_choice = input(Fore.GREEN + "Do you want to add this movie? (yes/no): ").strip().lower()
                    
                    if add_movie_choice == "yes":
                        movie_id = self.add_movie(movie_name)  # Add movie and get its ID
                        if movie_id is None:
                            print("Failed to add movie. Try again.")
                            continue  # Restart loop
                    else:
                        print(Fore.RED + "Movie not added. Try another movie or type 'back' to exit.")
                        continue  # Restart loop to enter another movie

                # Step 6: Check if the actor is already linked to the movie
                self.cursor.execute("SELECT * FROM Movie_Actor WHERE movie_id = %s AND actor_id = %s", (movie_id, actor_id))
                existing_link = self.cursor.fetchone()

                if existing_link:
                    print(Fore.RED + f"Actor '{actor_name}' is already added to movie '{movie_name}'.")
                    continue  # Ask for another movie

                # Step 7: Insert into the Movie_Actor table
                query = "INSERT INTO Movie_Actor (movie_id, actor_id) VALUES (%s, %s)"
                self.cursor.execute(query, (movie_id, actor_id))
                self.db.conn.commit()

                print(Fore.WHITE + f"Actor '{actor_name}' successfully added to movie '{movie_name}'.")

        except Exception as e:
            print(Fore.RED + f"Error adding actor to movie: {e}")
            
    def add_movie_to_actor(self):
        """Adds a movie to one or multiple actors after verifying their existence in the database."""
        try:
            # Step 1: Check if movies exist
            if not self.movies:
                print(Fore.RED + "No movies found.")
                return

            # Step 2: Take movie name and check if it exists
            movie_name = input("Enter the movie name: ").strip()

            movie_id = None
            for mid, movie_info in self.movies.items():
                if movie_info["movie_name"].lower() == movie_name.lower():
                    movie_id = mid
                    break

            if movie_id is None:
                print(Fore.RED + f"Movie '{movie_name}' does not exist.")
                add_movie_choice = input(Fore.GREEN + "Do you want to add this movie? (yes/no): ").strip().lower()

                if add_movie_choice == "yes":
                    movie_id = self.add_movie(movie_name)  # Add movie and get its ID
                    if movie_id is None:
                        print("Failed to add movie. Try again.")
                        return  # Stop the process
                else:
                    print(Fore.RED + "Movie not added. Returning to main menu.")
                    return

            # Step 3: Check if actors exist
            if not self.actors:
                print(Fore.RED + "No actors found. Please add an actor first.")
                return

            while True:
                # Step 4: Take actor name
                actor_name = input("\nEnter the actor's name (or type 'back' to exit): ").strip()

                if actor_name.lower() == "back":
                    print(Fore.BLUE + "Returning to the main menu...")
                    return  # Exit the loop and return

                # Step 5: Check if actor exists
                actor_id = None
                for aid, actor_info in self.actors.items():
                    if actor_info["name"].lower() == actor_name.lower():  # FIXED: Correct key
                        actor_id = aid
                        break

                if actor_id is None:
                    print(Fore.RED + f"Actor '{actor_name}' does not exist.")
                    add_actor_choice = input(Fore.GREEN + "Do you want to add this actor? (yes/no): ").strip().lower()

                    if add_actor_choice == "yes":
                        actor_id = self.add_actor(actor_name)  # Add actor and get its ID
                        if actor_id is None:
                            print("Failed to add actor. Try again.")
                            continue  # Restart loop
                    else:
                        print(Fore.RED + "Actor not added. Try another actor or type 'back' to exit.")
                        continue  # Restart loop to enter another actor

                # Step 6: Check if the actor is already linked to the movie
                self.cursor.execute(
                    "SELECT * FROM Movie_Actor WHERE movie_id = %s AND actor_id = %s",
                    (movie_id, actor_id),
                )
                existing_link = self.cursor.fetchone()

                if existing_link:
                    print(Fore.RED + f"Actor '{actor_name}' is already added to movie '{movie_name}'.")
                    continue  # Ask for another actor

                # Step 7: Insert into the Movie_Actor table
                query = "INSERT INTO Movie_Actor (movie_id, actor_id) VALUES (%s, %s)"
                self.cursor.execute(query, (movie_id, actor_id))
                self.db.conn.commit()

                print(Fore.WHITE + f"Movie '{movie_name}' successfully assigned to actor '{actor_name}'.")

        except Exception as e:
            print(Fore.RED + f"Error adding movie to actor: {e}")

    def add_director_to_movie(self):
        """Adds a director to one or multiple movies after verifying their existence in the database."""
        try:
            # Step 1: Check if directors exist
            if not self.directors:
                print(Fore.RED + "No directors found.")
                return

            # Step 2: Take director name and check if they exist
            director_name = input("Enter the director's name: ").strip()

            director_id = None
            for did, director_info in self.directors.items():
                if director_info["director_name"].lower() == director_name.lower():
                    director_id = did
                    break

            if director_id is None:
                print(Fore.RED + f"Director '{director_name}' does not exist.")
                return

            # Step 3: Check if movies exist
            if not self.movies:
                print(Fore.RED + "No movies found. Please add a movie first.")
                return

            while True:
                # Step 4: Take movie name
                movie_name = input("\nEnter the movie name (or type 'back' to exit): ").strip()

                if movie_name.lower() == "back":
                    print("Returning to the main menu...")
                    return  # Exit the loop and return

                # Step 5: Check if movie exists
                movie_id = None
                for mid, movie_info in self.movies.items():
                    if movie_info["movie_name"].lower() == movie_name.lower():
                        movie_id = mid
                        break

                if movie_id is None:
                    print(Fore.RED + f"Movie '{movie_name}' does not exist.")
                    add_movie_choice = input(Fore.GREEN + "Do you want to add this movie? (yes/no): ").strip().lower()
                    
                    if add_movie_choice == "yes":
                        movie_id = self.add_movie(movie_name)  # Add movie and get its ID
                        if movie_id is None:
                            print("Failed to add movie. Try again.")
                            continue  # Restart loop
                    else:
                        print(Fore.RED + "Movie not added. Try another movie or type 'back' to exit.")
                        continue  # Restart loop to enter another movie

                # Step 6: Check if the director is already linked to the movie
                self.cursor.execute("SELECT * FROM Movie_Director WHERE movie_id = %s AND director_id = %s", (movie_id, director_id))
                existing_link = self.cursor.fetchone()

                if existing_link:
                    print(Fore.RED + f"Director '{director_name}' is already assigned to movie '{movie_name}'.")
                    continue  # Ask for another movie

                # Step 7: Insert into the Movie_Director table
                query = "INSERT INTO Movie_Director (movie_id, director_id) VALUES (%s, %s)"
                self.cursor.execute(query, (movie_id, director_id))
                self.db.conn.commit()

                print(Fore.WHITE + f"Director '{director_name}' successfully added to movie '{movie_name}'.")

        except Exception as e:
            print(Fore.RED + f"Error adding director to movie: {e}")
 
    def add_movie_to_director(self):
        """Adds a director to a movie after verifying their existence in the database."""
        try:
            # Step 1: Check if movies exist
            if not self.movies:
                print(Fore.RED + "No movies found.")
                return

            # Step 2: Take movie name and check if it exists
            movie_name = input("Enter the movie name: ").strip()

            movie_id = None
            for mid, movie_info in self.movies.items():
                if movie_info["movie_name"].lower() == movie_name.lower():
                    movie_id = mid
                    break

            if movie_id is None:
                print(Fore.RED + f"Movie '{movie_name}' does not exist.")
                return
                
            if not self.directors:
                print(Fore.RED + "No directors found. Please add a director first.")
                return

            while True:
                # Step 4: Take director name
                director_name = input("\nEnter the director's name (or type 'back' to exit): ").strip()

                if director_name.lower() == "back":
                    print(Fore.BLUE + "Returning to the main menu...")
                    return  # Exit the loop and return

                # Step 5: Check if director exists
                director_id = None
                for did, director_info in self.directors.items():
                    if director_info["director_name"].lower() == director_name.lower():
                        director_id = did
                        break

                if director_id is None:
                    print(Fore.RED + f"Director '{director_name}' does not exist.")
                    add_director_choice = input(Fore.GREEN + "Do you want to add this director? (yes/no): ").strip().lower()

                    if add_director_choice == "yes":
                        director_id = self.add_director(director_name)  # Add director and get ID
                        if director_id is None:
                            print("Failed to add director. Try again.")
                            continue  # Restart loop
                    else:
                        print(Fore.RED + "Director not added. Try another director or type 'back' to exit.")
                        continue  # Restart loop to enter another director

                # Step 6: Check if the director is already linked to the movie
                self.cursor.execute(
                    "SELECT * FROM Movie_Director WHERE movie_id = %s AND director_id = %s",
                    (movie_id, director_id),
                )
                existing_link = self.cursor.fetchone()

                if existing_link:
                    print(Fore.RED + f"Director '{director_name}' is already linked to movie '{movie_name}'.")
                    continue  # Ask for another director

                # Step 7: Insert into the Movie_Director table
                query = "INSERT INTO Movie_Director (movie_id, director_id) VALUES (%s, %s)"
                self.cursor.execute(query, (movie_id, director_id))
                self.db.conn.commit()

                print(Fore.WHITE + f"Movie '{movie_name}' successfully assigned to director '{director_name}'.")

        except Exception as e:
            print(Fore.RED + f"Error adding director to movie: {e}")

    def add_movie_to_rating(self):
        """Allows users to rate a movie after verifying both movie and user existence in the database."""
        try:
            # Step 1: Check if movies exist
            if not self.movies:
                print(Fore.RED + "No movies found in the database. Please add a movie first.")
                return

            # Step 2: Ask for the movie name
            while True:
                movie_name = input("Enter the movie name: ").strip()
                
                # Check if movie exists
                movie_id = None
                for mid, movie_info in self.movies.items():
                    if movie_info["movie_name"].lower() == movie_name.lower():
                        movie_id = mid
                        break
                
                if movie_id is None:
                    print(Fore.RED + f"Movie '{movie_name}' does not exist.")
                    return
                    # add_movie_choice = input("Do you want to add this movie? (yes/no): ").strip().lower()

                    # if add_movie_choice == "yes":
                    #     movie_id = self.add_movie(movie_name)  # Add movie and get its ID
                    #     if movie_id is None:
                    #         print("Failed to add movie. Try again.")
                    #         continue  # Restart movie input
                    # else:
                    #     print("Returning to the main menu.")
                    #     return

                break  # Exit movie input loop if movie found or added successfully

            # Step 3: Ask for user name
            while True:
                user_name = input("Enter the user name: ").strip()

                # Check if user exists
                user_id = None
                for uid, user_info in self.users.items():
                    if user_info["user_name"].lower() == user_name.lower():
                        user_id = uid
                        break

                if user_id is None:
                    print(Fore.RED + f"User '{user_name}' does not exist.")
                    add_user_choice = input(Fore.GREEN + "Do you want to add this user? (yes/no): ").strip().lower()

                    if add_user_choice == "yes":
                        user_id = self.add_user(user_name)  # Add user and get their ID
                        if user_id is None:
                            print("Failed to add user. Try again.")
                            continue  # Restart user input
                    else:
                        print(Fore.RED + "Returning to the main menu.")
                        return
 
                break  # Exit user input loop if user found or added successfully

            # Step 4: Ask for rating (validate between 1-5)
            while True:
                try:
                    rating = float(input("Enter rating (1 to 10): "))
                    if 1 <= rating <= 10:
                        break
                    else:
                        print(Fore.RED + "Invalid rating. Please enter a number between 1 and 10.")
                except ValueError:
                    print(Fore.RED + "Invalid input. Please enter a numeric value.")

            # Step 5: Insert rating into the database
            query = "INSERT INTO User_Rating (movie_id, user_id, rating) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (movie_id, user_id, rating))
            self.db.conn.commit()

            print(Fore.WHITE + f"Rating of {rating} added for movie '{movie_name}' by user '{user_name}'.")

        except Exception as e:
            print(Fore.RED + f"Error adding movie rating: {e}")

    def plot_movies_by_director(self):
        query = """
        SELECT d.director_name, COUNT(m.movie_id)
        FROM Directors d
        JOIN movie_director md ON d.director_id = md.director_id
        JOIN Movies m ON md.movie_id = m.movie_id
        GROUP BY d.director_name
        """
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        if not data:
            print(Fore.RED + "No director data found for visualization.")
            return

        directors, movie_counts = zip(*data)

        plt.figure(figsize=(10, 6))
        sns.barplot(x=list(directors), y=list(movie_counts), hue=list(directors), palette="viridis", legend=False)
        plt.xticks(rotation=45)
        plt.xlabel("Directors")
        plt.ylabel("Number of Movies")
        plt.title("Movies Directed by Each Director")
        plt.show()

    def exit_system(self):
        """ Close database connections properly before exiting """
        try:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
                print(Fore.WHITE + "Cursor closed.")

            if hasattr(self, 'db') and self.db:
                self.db.close()
                print(Fore.WHITE + "Database connection closed.")

        except Exception as e:
            print(Fore.RED + f"Error while closing database connection: {e}")

        print(Fore.WHITE + "Exiting system...")
        
        sys.exit(0)  # Properly exit the program
