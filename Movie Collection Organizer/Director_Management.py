from Movie_Collection import MovieCollection
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from tabulate import tabulate
from colorama import init, Fore, Style

init(autoreset=True)

class DirectorManagement(MovieCollection):
    def manage_directors(self):
        while True:
            options = [
                "Add Director 🆕",
                "Update Director ✏️",
                "Remove Director ❌",
                "List Directors 📋",
                "Include Director in Movie 🎬",
                "Get Director's Movies 🎥",
                "Back 🔙"
            ]
            
            self.display_menu("Director Management", options)
            choice = self.get_user_choice(options)
            if choice == 1:
                self.add_director()
            elif choice == 2:
                self.update_director()
            elif choice == 3:
                self.remove_director()
            elif choice == 4:
                self.list_directors()
            elif choice == 5:
                self.add_director_to_movie()                
            elif choice == 6:
                self.get_director_movies()
            elif choice == 7:
                break
            
    def add_director(self, add_name=None):
        """Adds a new director to the database and updates the in-memory self.directors dictionary.
        If add_name is provided, it uses that instead of prompting the user.
        Returns the director_id of the newly added or existing director.
        """
        try:
            # Use provided name or ask for input
            director_name = add_name.strip() if add_name else input(Fore.GREEN + "Enter director name: ").strip()

            # Validate if director already exists
            for director_id, director in self.directors.items():
                if director["director_name"].lower() == director_name.lower():
                    print(Fore.RED + f"Director '{director_name}' already exists.")
                    return director_id  # Return existing director_id
                
            # Get birth date if not using add_name
            birth_date = self.get_valid_date("new ")   # Can be modified as needed

            # Get gender if not using add_name
            gender = None
            # if  add_name:
            gender = input(Fore.GREEN + "Enter gender (Male/Female): ").strip().capitalize()
            if gender not in ["Male", "Female"]:
                print(Fore.RED + "Invalid gender. Please enter Male or Female.")
                return None

            # Insert into database
            query = "INSERT INTO Directors (director_name, birth_date, gender) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (director_name, birth_date, gender))
            self.db.conn.commit()

            # Get the new director's ID
            director_id = self.cursor.lastrowid

            # Update self.directors dictionary
            self.directors[director_id] = {
                "director_name": director_name,
                "birth_date": birth_date,
                "gender": gender
            }

            print(Fore.WHITE + f"Director '{director_name}' added successfully.")
            return director_id  # Return new director_id
        except Exception as e:
            print(Fore.RED + f"Error adding director: {e}")
            return None


    def list_directors(self):
        """Displays all directors' information except director_id using self.directors."""
        if not self.directors:
            print(Fore.RED + "No directors found in memory.")
            return

        # Prepare data for tabulation (excluding director_id)
        table_data = [
            [director["director_name"], director["birth_date"], director["gender"]]
            for director in self.directors.values()
        ]

        # Define table headers
        headers = ["Director Name", "Birth Date", "Gender"]

        # Print formatted table
        print(Fore.WHITE + tabulate(table_data, headers=headers, tablefmt="grid"))

    def remove_director(self):
        """Removes a director from the database and updates self.directors."""
        try:
            director_name = input(Fore.GREEN + "Enter the director name to remove: ").strip()

            # Find the director in self.directors
            director_id_to_remove = None
            for director_id, director in self.directors.items():
                if director["director_name"].lower() == director_name.lower():
                    director_id_to_remove = director_id
                    break

            # If director is not found
            if director_id_to_remove is None:
                print(Fore.RED + f"Director '{director_name}' not found.")
                return

            # Delete from database
            query = "DELETE FROM Directors WHERE director_id = %s"
            self.cursor.execute(query, (director_id_to_remove,))
            self.db.conn.commit()

            # Remove from self.directors dictionary
            del self.directors[director_id_to_remove]

            print(Fore.WHITE + f"Director '{director_name}' removed successfully.")

        except Exception as e:
            print(Fore.RED + f"Error removing director: {e}")

    def update_director(self):
        """Prompts the user for a director name and updates their details if they exist."""
        director_name = input(Fore.GREEN + "Enter director name to update: ").strip()

        # Search for the director in self.directors
        director_id = None
        for id_, director in self.directors.items():
            if director["director_name"].lower() == director_name.lower():
                director_id = id_
                break

        if director_id is None:
            print(Fore.RED + "Director not found.")
            return

        print(Fore.YELLOW + '(Leave blank to keep unchanged):')
        birth_date = input(Fore.GREEN + 'Enter birth date (YYYY-MM-DD):')
        if birth_date:
            birth_date = birth_date.strip()
            birth_date = self.get_valid_date("new",birth_date)
            
        else:
            birth_date = None
        gender = input(Fore.GREEN + "Enter new gender (Male/Female): ").strip().capitalize()

        if gender and gender not in ["Male", "Female"]:
            print(Fore.RED + "Invalid gender. Please enter 'Male' or 'Female'.")
            return

        update_fields = []
        update_values = []

        if birth_date:
            update_fields.append("birth_date = %s")
            update_values.append(birth_date)
        if gender:
            update_fields.append("gender = %s")
            update_values.append(gender)

        if not update_fields:
            print(Fore.RED + "No valid fields to update.")
            return

        update_values.append(director_id)
        query = f"UPDATE Directors SET {', '.join(update_fields)} WHERE director_id = %s"

        try:
            self.cursor.execute(query, update_values)
            self.db.conn.commit()

            # Update self.directors dictionary
            if birth_date:
                self.directors[director_id]["birth_date"] = birth_date
            if gender:
                self.directors[director_id]["gender"] = gender

            print(Fore.WHITE + "Director updated successfully.")
        except mysql.connector.Error as err:
            print(Fore.RED + "Error:", err)

    def get_director_movies(self, director_name=None):
        """Retrieves all movies directed by a given director, prints them in tabular format,
        and optionally saves the data to a PDF file."""
        try:
            # Get director name from user if not provided
            if director_name is None:
                director_name = input(Fore.GREEN + "Enter director's name: ").strip()

            # Query to get the director ID
            query = "SELECT director_id FROM Directors WHERE director_name = %s"
            self.cursor.execute(query, (director_name,))
            director = self.cursor.fetchone()

            if not director:
                print(Fore.RED + f"Director '{director_name}' not found.")
                return

            director_id = director[0]

            # Query to get movies directed by the director
            query = """
            SELECT m.movie_name 
            FROM Movies m
            JOIN movie_director md ON m.movie_id = md.movie_id
            WHERE md.director_id = %s
            """
            self.cursor.execute(query, (director_id,))
            movies = self.cursor.fetchall()

            if not movies:
                print(Fore.RED + f"No movies found for director '{director_name}'.")
                return

            # Prepare data for display (Adding serial numbers)
            movie_data = [[i + 1, movie[0]] for i, movie in enumerate(movies)]

            # Print tabulated output in the console
            print(Fore.WHITE + "\nMovies directed by '{}':".format(director_name))
            print(Fore.WHITE + tabulate(movie_data, headers=["Movie Number", "Movie Name"], tablefmt="grid", colalign=("center", "center")))

            # Ask user if they want to save the data to a PDF
            choice = input(Fore.GREEN + "\nDo you want to save this data to a PDF? (yes/no): ").strip().lower()
            if choice not in ["yes", "y"]:
                print(Fore.YELLOW + "Skipping PDF generation.")
                return

            # Generate PDF
            pdf_filename = f"{director_name}_movies.pdf"
            doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
            elements = []

            # Add title
            styles = getSampleStyleSheet()
            title = Paragraph(f"<b>Movies Directed by '{director_name}'</b>", styles["Title"])
            elements.append(title)

            # Create table with headers
            table_data = [["Movie Number", "Movie Name"]] + movie_data
            table = Table(table_data, colWidths=[100, 300])  # Adjust column widths if necessary

            # Style the table
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Align text center for all cells
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),  # Vertically align to middle
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]))

            elements.append(table)

            # Build the PDF
            doc.build(elements)

            print(Fore.WHITE + f"Movies directed by '{director_name}' saved to '{pdf_filename}'.")

        except Exception as e:
            print(Fore.RED + f"Error retrieving movies for director: {e}")