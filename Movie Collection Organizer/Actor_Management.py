from Movie_Collection import MovieCollection
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from tabulate import tabulate  # Import tabulate for console output
import matplotlib.pyplot as plt
import numpy as np
from colorama import init, Fore, Style

init(autoreset=True)

class ActorManagement(MovieCollection):
    def manage_actors(self):
        while True:
            options = [
                "Add Actor 🆕",
                "Update Actor ✏️",
                "Remove Actor ❌",
                "List Actors 📋",
                "Include Actor in Movie 🎬",
                "Get Actor's Movies 🎥",
                "Back 🔙"
            ]
            
            self.display_menu("Actor Management", options)
            choice = self.get_user_choice(options)
            if choice == 1:
                self.add_actor()
            elif choice == 2:
                self.update_actor()
            elif choice == 3:
                self.remove_actor()
            elif choice == 4:
                self.list_actors()
            elif choice == 5:
                self.add_actor_to_movie()                
            elif choice == 6:
                self.get_movies_by_actor()
            elif choice == 7:
                break
    
    def add_actor(self, actor_name=None):
        """Add a new actor to the database and update the in-memory actors dictionary."""
        try:
            if actor_name is None:
                actor_name = input(Fore.GREEN + "Enter actor's name: ").strip()

            for actor_id, actor_info in self.actors.items():
                if actor_info["name"].lower() == actor_name.lower():
                    print(Fore.RED + f"Actor '{actor_name}' already exists.")
                    return actor_id

            if actor_name is None:
                return None

            birth_date = self.get_valid_date("")
            gender = input(Fore.GREEN + "Enter gender (Male/Female): ").strip().capitalize()

            if gender not in ["Male", "Female"]:
                print(Fore.RED + "Invalid gender. Please enter 'Male' or 'Female'.")
                return None

            query = "INSERT INTO Actors (actor_name, birth_date, gender) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (actor_name, birth_date, gender))
            self.db.conn.commit()

            actor_id = self.cursor.lastrowid

            self.actors[actor_id] = {
                "name": actor_name,
                "birth_date": birth_date,
                "gender": gender
            }

            print(Fore.WHITE + f"Actor '{actor_name}' added successfully.")
            return actor_id

        except Exception as e:
            print(Fore.RED + f"Error adding actor: {e}")
            return None

    def remove_actor(self):
        """Remove an actor by name from the database, Movie_Actor table, and the in-memory actors dictionary."""
        try:
            if not self.actors:
                print(Fore.RED + "No actors available to remove.")
                return

            actor_name = input(Fore.GREEN + "Enter the name of the actor to remove: ").strip()

            actor_id = None
            for key, actor_info in self.actors.items():
                if actor_info['name'].lower() == actor_name.lower():
                    actor_id = key
                    break

            if actor_id is None:
                print(Fore.RED + f"Actor '{actor_name}' not found.")
                return

            query = "DELETE FROM Actors WHERE actor_id = %s"
            self.cursor.execute(query, (actor_id,))
            self.db.conn.commit()

            removed_actor = self.actors.pop(actor_id)

            print(Fore.WHITE + f"Actor '{removed_actor['name']}' (ID: {actor_id}) has been successfully removed.")
        except Exception as e:
            print(Fore.RED + f"Error removing actor: {e}")

    def update_actor(self):
        """Prompts the user for an actor name and updates their details if they exist."""
        actor_name = input(Fore.GREEN + "Enter actor name to update: ").strip()

        actor_id = None
        for id_, actor in self.actors.items():
            if actor["name"].lower() == actor_name.lower():
                actor_id = id_
                break

        if actor_id is None:
            print(Fore.RED + "Actor not found.")
            return

        print(Fore.YELLOW + "(Leave blank to keep unchanged):")
        birth_date = input(Fore.GREEN + 'Enter new birth date (YYYY-MM-DD): ')
        if birth_date:
            birth_date = birth_date.strip()
            birth_date = self.get_valid_date("new ",birth_date)
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

        update_values.append(actor_id)
        query = f"UPDATE Actors SET {', '.join(update_fields)} WHERE actor_id = %s"

        try:
            self.cursor.execute(query, update_values)
            self.db.conn.commit()

            if birth_date:
                self.actors[actor_id]["birth_date"] = birth_date
            if gender:
                self.actors[actor_id]["gender"] = gender

            print(Fore.WHITE + "Actor updated successfully.")
        except mysql.connector.Error as err:
            print(Fore.RED + "Error:", err)

    def list_actors(self):
        """Prints all actors in a tabulated format."""
        if not self.actors:
            print(Fore.RED + "No actors found.")
            return

        table_data = [[actor["name"], actor["birth_date"], actor["gender"]] 
                    for actor in self.actors.values()]
        
        headers = ["Name", "Birth Date", "Gender"]
        print(Fore.WHITE + tabulate(table_data, headers=headers, tablefmt="grid"))

    def get_movies_by_actor(self, actor_name=None):
        """Retrieves movies associated with a given actor, prints in tabular form, and optionally saves to a PDF file."""
        try:
            if actor_name is None:
                actor_name = input(Fore.GREEN + "Enter actor name: ").strip()

            query = "SELECT actor_id FROM Actors WHERE actor_name = %s"
            self.cursor.execute(query, (actor_name,))
            actor_id = self.cursor.fetchone()
            self.cursor.fetchall() 
            
            if not actor_id:
                print(Fore.RED + f"Actor '{actor_name}' not found.")
                return

            query = """
            SELECT m.movie_name 
            FROM Movies m 
            JOIN movie_actor ma ON m.movie_id = ma.movie_id 
            WHERE ma.actor_id = %s
            """
            self.cursor.execute(query, (actor_id[0],))
            movies = self.cursor.fetchall()

            if not movies:
                print(Fore.RED + f"No movies found for the actor '{actor_name}'.")
                return

            movie_names = [[i + 1, movie[0]] for i, movie in enumerate(movies)]  

            print(Fore.WHITE + f"\nMovies featuring '{actor_name}':")
            print(Fore.WHITE + tabulate(movie_names, headers=["Movie Number", "Movie Name"], tablefmt="grid", colalign=("center", "center")))

            choice = input(Fore.GREEN + "\nDo you want to save this data to a PDF? (yes/no): ").strip().lower()
            if choice not in ["yes", "y"]:
                print(Fore.YELLOW + "Skipping PDF generation.")
                return

            pdf_filename = f"{actor_name}_movies.pdf"
            doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
            elements = []

            styles = getSampleStyleSheet()
            title = Paragraph(f"<b>Movies featuring '{actor_name}'</b>", styles["Title"])
            elements.append(title)

            table_data = [["Movie Number", "Movie Name"]] + movie_names
            table = Table(table_data, colWidths=[100, 300])

            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black)
            ]))

            elements.append(table)

            doc.build(elements)

            print(Fore.WHITE + f"\nMovies featuring '{actor_name}' saved to '{pdf_filename}'.")

        except Exception as e:
            print(Fore.RED + f"Error retrieving movies: {e}")

