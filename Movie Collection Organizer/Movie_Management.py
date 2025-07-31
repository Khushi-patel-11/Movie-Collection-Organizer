from Movie_Collection import MovieCollection
from tabulate import tabulate
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from decimal import Decimal
from colorama import init, Fore, Style

init(autoreset=True)

class MovieManagement(MovieCollection):
    def manage_movies(self):
        while True:
            options = [
                "Add Movie 🎬",
                "Update Movie ✏️",
                "Remove Movie ❌",
                "List Movies 📋",
                "Include Movie in Actor 🎭",
                "Include Movie in Director 🎥",
                "Add rating to Movie ⭐", 
                "Get Actor's Movies 🎭",
                "Get Director's Movie 🎥",
                "Get Movie's Rating ⭐",
                "Back 🔙"
            ]
            self.display_menu("Movie Management", options)
            choice = self.get_user_choice(options)
            if choice == 1:
                self.add_movie()
            elif choice == 2:
                self.update_movie()
            elif choice == 3:
                self.remove_movie()
            elif choice == 4:
                self.list_movies()
            elif choice == 5:
                self.add_movie_to_actor()
            elif choice == 6:
                self.add_movie_to_director()
            elif choice == 7:
                self.add_movie_to_rating()
            elif choice == 8:
                self.get_actors_by_movie()
            elif choice == 9:
                self.get_directors_by_movie()
            elif choice == 10:
                self.get_movie_ratings()
            elif choice == 11:
                break
            
    def add_movie(self, movie_name=None):
        """Adds a new movie to the database and updates the in-memory movies dictionary."""
        try:
            if movie_name is None:
                movie_name = input(Fore.GREEN + "Enter movie name: ").strip()

            for movie_id, movie in self.movies.items():
                if movie["movie_name"].lower() == movie_name.lower():
                    print(Fore.RED + f"Movie '{movie_name}' already exists.")
                    return movie_id
            
            released_year = input(Fore.GREEN + "Enter released year: ").strip()
            genre = input(Fore.GREEN + "Enter genre: ").strip()
            duration = input(Fore.GREEN + "Enter duration (in minutes): ").strip()

            try:
                released_year = int(released_year)
                if released_year < 1800:
                    raise ValueError("Year should be 1800 or later.")
            except ValueError:
                print(Fore.RED + "Invalid released year. Please enter a valid year (e.g., 2023).")
                return None

            try:
                duration = int(duration)
                if duration <= 0:
                    raise ValueError("Duration must be a positive number.")
            except ValueError:
                print(Fore.RED + "Invalid duration. Please enter a valid number (e.g., 120).")
                return None

            if not genre:
                print(Fore.RED + "Genre cannot be empty.")
                return None

            query = "INSERT INTO Movies (movie_name, duration, released_year, genre) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (movie_name, duration, released_year, genre))
            movie_id = self.cursor.lastrowid
            self.db.conn.commit()

            self.movies[movie_id] = {
                "movie_name": movie_name,
                "released_year": released_year,
                "genre": genre,
                "duration": duration
            }

            print(Fore.WHITE + f"Movie '{movie_name}' added successfully.")
            return movie_id

        except Exception as e:
            print(Fore.RED + f"Error adding movie: {e}")
            return None

    def list_movies(self):
        """Displays all movies using self.movies dictionary in a tabulated format, excluding movie_id."""
        if not self.movies:
            print(Fore.RED + "No movies available.")
            return

        table_data = [
            [movie["movie_name"], movie["released_year"], movie["genre"], movie["duration"]]
            for movie in self.movies.values()
        ]

        headers = ["Movie Name", "Released Year", "Genre", "Duration (mins)"]

        print(Fore.WHITE + tabulate(table_data, headers=headers, tablefmt="grid"))

    def remove_movie(self):
        """Removes a movie from the database and updates self.movies dictionary."""
        try:
            movie_name = input(Fore.GREEN + "Enter the movie name to remove: ").strip()

            movie_id_to_remove = None
            for movie_id, movie in self.movies.items():
                if movie["movie_name"].lower() == movie_name.lower():
                    movie_id_to_remove = movie_id
                    break

            if movie_id_to_remove is None:
                print(Fore.RED + f"Movie '{movie_name}' not found.")
                return

            query = "DELETE FROM Movies WHERE movie_id = %s"
            self.cursor.execute(query, (movie_id_to_remove,))
            self.db.conn.commit()

            del self.movies[movie_id_to_remove]

            print(Fore.WHITE + f"Movie '{movie_name}' removed successfully.")
        except Exception as e:
            print(Fore.RED + f"Error removing movie: {e}")

    def update_movie(self):
        """Updates movie details (released year, genre, duration) in the database and self.movies dictionary."""
        try:
            movie_name = input(Fore.GREEN + "Enter the movie name to update: ").strip()

            movie_id_to_update = None
            for movie_id, movie in self.movies.items():
                if movie["movie_name"].lower() == movie_name.lower():
                    movie_id_to_update = movie_id
                    break

            if movie_id_to_update is None:
                print(Fore.RED + f"Movie '{movie_name}' not found.")
                return

            new_released_year = input(Fore.GREEN + "Enter new released year: ").strip()
            new_genre = input(Fore.GREEN + "Enter new genre: ").strip()
            new_duration = input(Fore.GREEN + "Enter new duration in minutes: ").strip()

            if new_released_year:
                try:
                    new_released_year = int(new_released_year)
                    if new_released_year < 1800:
                        raise ValueError("Year should be 1800 or later.")
                except ValueError:
                    print(Fore.RED + "Invalid released year. Please enter a valid year (e.g., 2023).")
                    return
            else:
                new_released_year = self.movies[movie_id_to_update]["released_year"]

            if new_duration:
                try:
                    new_duration = int(new_duration)
                    if new_duration <= 0:
                        raise ValueError("Duration must be a positive number.")
                except ValueError:
                    print(Fore.RED + "Invalid duration. Please enter a valid number (e.g., 120).")
                    return
            else:
                new_duration = self.movies[movie_id_to_update]["duration"]

            if not new_genre:
                new_genre = self.movies[movie_id_to_update]["genre"]

            query = "UPDATE Movies SET released_year = %s, genre = %s, duration = %s WHERE movie_id = %s"
            self.cursor.execute(query, (new_released_year, new_genre, new_duration, movie_id_to_update))
            self.db.conn.commit()

            self.movies[movie_id_to_update] = {
                "movie_name": movie_name,
                "released_year": new_released_year,
                "genre": new_genre,
                "duration": new_duration
            }

            print(Fore.WHITE + f"Movie '{movie_name}' updated successfully.")
        except Exception as e:
            print(Fore.RED + f"Error updating movie: {e}")

    def generate_movie_report(self, filename="movie_report"):
        """Generates a movie report and saves it as CSV & PDF."""
        if not self.movies:
            print(Fore.RED + "No movie data available to generate report.")
            return

        df = pd.DataFrame(self.movies.values())

        csv_file = f"{filename}.csv"
        df.to_csv(csv_file, index=False)
        print(Fore.WHITE + f"Report saved as {csv_file}")

        pdf_file = f"{filename}.pdf"
        self.save_report_as_pdf(df, pdf_file)

    def save_report_as_pdf(self, df, filename):
        """Saves the DataFrame as a formatted PDF file."""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axis("tight")
        ax.axis("off")
        ax.table(cellText=df.values, colLabels=df.columns, cellLoc="center", loc="center")

        plt.savefig(filename, format="pdf", bbox_inches="tight")
        print(Fore.WHITE + f"Report saved as {filename}")

    def get_actors_by_movie(self, movie_name=None):
        """Retrieves actors associated with a given movie, prints in tabular form, and optionally saves it to a PDF file."""
        try:
            if movie_name is None:
                movie_name = input(Fore.GREEN + "Enter movie name: ").strip()

            query = "SELECT movie_id FROM Movies WHERE movie_name = %s"
            self.cursor.execute(query, (movie_name,))
            movie_id = self.cursor.fetchone()

            if not movie_id:
                print(Fore.RED + f"Movie '{movie_name}' not found.")
                return

            query = """
            SELECT a.actor_name 
            FROM Actors a 
            JOIN movie_actor ma ON a.actor_id = ma.actor_id 
            WHERE ma.movie_id = %s
            """
            self.cursor.execute(query, (movie_id[0],))
            actors = self.cursor.fetchall()

            if not actors:
                print(Fore.RED + f"No actors found for the movie '{movie_name}'.")
                return

            actor_names = [[i + 1, actor[0]] for i, actor in enumerate(actors)]  

            print(Fore.WHITE + "\nActors in '{}':".format(movie_name))
            print(Fore.WHITE + tabulate(actor_names, headers=["Actor Number", "Actor Name"], tablefmt="grid", colalign=("center", "center")))

            choice = input(Fore.GREEN + "\nDo you want to save this data to a PDF? (yes/no): ").strip().lower()
            if choice not in ["yes", "y"]:
                print(Fore.YELLOW + "Skipping PDF generation.")
                return

            pdf_filename = f"{movie_name}_actors.pdf"
            doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
            elements = []

            styles = getSampleStyleSheet()
            title = Paragraph(f"<b>Actors in '{movie_name}'</b>", styles["Title"])
            elements.append(title)

            table_data = [["Actor Number", "Actor Name"]] + actor_names
            table = Table(table_data, colWidths=[100, 300])

            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)

            doc.build(elements)

            print(Fore.WHITE + f"Actors for movie '{movie_name}' saved to '{pdf_filename}'.")

        except Exception as e:
            print(Fore.RED + f"Error retrieving actors: {e}")

    def get_directors_by_movie(self, movie_name=None):
        """Retrieves directors associated with a given movie, prints them in tabular format, and optionally saves to a PDF."""
        try:
            if movie_name is None:
                movie_name = input(Fore.GREEN + "Enter movie name: ").strip()

            query = "SELECT movie_id FROM Movies WHERE movie_name = %s"
            self.cursor.execute(query, (movie_name,))
            movie = self.cursor.fetchone()

            if not movie:
                print(Fore.RED + f"Movie '{movie_name}' not found.")
                return

            movie_id = movie[0]

            query = """
            SELECT d.director_name 
            FROM Directors d 
            JOIN movie_director md ON d.director_id = md.director_id 
            WHERE md.movie_id = %s
            """
            self.cursor.execute(query, (movie_id,))
            directors = self.cursor.fetchall()

            if not directors:
                print(Fore.RED + f"No directors found for the movie '{movie_name}'.")
                return

            director_names = [[i + 1, director[0]] for i, director in enumerate(directors)]

            print(Fore.WHITE + "\nDirectors for '{}':".format(movie_name))
            print(Fore.WHITE + tabulate(director_names, headers=["Director Number", "Director Name"], tablefmt="grid", colalign=("center", "center")))

            choice = input(Fore.GREEN + "\nDo you want to save this data to a PDF? (yes/no): ").strip().lower()
            if choice not in ["yes", "y"]:
                print(Fore.YELLOW + "Skipping PDF generation.")
                return

            pdf_filename = f"{movie_name}_directors.pdf"
            doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
            elements = []

            styles = getSampleStyleSheet()
            title = Paragraph(f"<b>Directors for '{movie_name}'</b>", styles["Title"])
            elements.append(title)
            elements.append(Spacer(1, 12))

            table_data = [["Director Number", "Director Name"]] + director_names
            table = Table(table_data, colWidths=[100, 350])

            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12)
            ]))

            elements.append(table)

            doc.build(elements)

            print(Fore.WHITE + f"Directors for movie '{movie_name}' saved to '{pdf_filename}'.")

        except Exception as e:
            print(Fore.RED + f"Error retrieving directors: {e}")

    def get_movie_ratings(self, movie_name=None):
        """Retrieves user ratings for a given movie, prints them in tabular format without User ID, 
        shows the average rating, and optionally saves the data to a PDF file."""
        try:
            if movie_name is None:
                movie_name = input(Fore.GREEN + "Enter movie name: ").strip()

            query = "SELECT movie_id FROM Movies WHERE movie_name = %s"
            self.cursor.execute(query, (movie_name,))
            movie = self.cursor.fetchone()

            if not movie:
                print(Fore.RED + f"Movie '{movie_name}' not found.")
                return

            movie_id = movie[0]

            query = """
            SELECT u.user_name, r.rating
            FROM Users u
            JOIN user_rating r ON u.user_id = r.user_id
            WHERE r.movie_id = %s
            """
            self.cursor.execute(query, (movie_id,))
            ratings = self.cursor.fetchall()

            if not ratings:
                print(Fore.RED + f"No ratings found for the movie '{movie_name}'.")
                return

            rating_data = [[i + 1, user_name, rating] for i, (user_name, rating) in enumerate(ratings)]
            avg_rating = sum(rating for _, _, rating in rating_data) / len(rating_data)

            print(Fore.WHITE + "\nRatings for '{}':".format(movie_name))
            print(Fore.WHITE + tabulate(rating_data, headers=["User Number", "User Name", "Movie Rating"], tablefmt="grid", colalign=("center", "center", "center")))
            print(Fore.WHITE + f"\nAverage Rating: {avg_rating:.2f} ⭐")

            choice = input(Fore.GREEN + "\nDo you want to save this data to a PDF? (yes/no): ").strip().lower()
            if choice not in ["yes", "y"]:
                print(Fore.YELLOW + "Skipping PDF generation.")
                return

            pdf_filename = f"{movie_name}_ratings.pdf"
            doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()

            title = Paragraph(f"<b>Ratings for '{movie_name}'</b>", styles["Title"])
            elements.append(title)
            elements.append(Spacer(1, 12))

            table_data = [["User Number", "User Name", "Movie Rating"]] + rating_data
            table = Table(table_data, colWidths=[100, 250, 150])

            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]))

            elements.append(table)
            elements.append(Spacer(1, 20))

            avg_rating_text = Paragraph(f"<b>Average Rating: {avg_rating:.2f}</b>", styles["Heading2"])
            elements.append(avg_rating_text)
            elements.append(Spacer(1, 10))

            doc.build(elements)
            print(Fore.WHITE + f"Ratings for movie '{movie_name}' saved to '{pdf_filename}'.")

        except Exception as e:
            print(Fore.RED + f"Error retrieving movie ratings: {e}")
    def autopct_format(self, pct):
        """Format percentages and adjust font size dynamically for small values."""
        if pct <= 2:
            return f'{pct:.1f}%'
        return f'{pct:.1f}%'




