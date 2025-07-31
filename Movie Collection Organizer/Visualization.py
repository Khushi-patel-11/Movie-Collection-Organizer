from Movie_Collection import MovieCollection
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
import numpy as np
from colorama import init, Fore, Style

init(autoreset=True)

class Visualization(MovieCollection):
    def visualization(self):
        while True:
            options = [
                "Movies by Genre (Bar Chart)",
                "Duration vs. Year (Scatter Plot)",
                "Movie Duration Distribution (Histogram)",
                "Average Movie Ratings (Bar Chart)",
                "Movies Per Actor (Bar Chart)",
                "Actor Gender Distribution (Pie Chart)",
                "Actor Movie Count Over Time (Line Chart)",
                "Top Directors by Movie Count (Bar Chart)",  
                "Users by Movie Ratings Given (Bar Chart)",
                "Back"
            ]
            
            self.display_menu("Visualization Menu", options)
            choice = self.get_user_choice(options)
            
            if choice == 1:
                self.plot_movies_by_genre()
            elif choice == 2:
                self.plot_duration_vs_year()
            elif choice == 3:
                self.plot_movie_duration_distribution()
            elif choice == 4:
                self.get_avg_ratings()
            elif choice == 5:
                self.visualize_movies_per_actor()
            elif choice == 6:
                self.visualize_actor_gender_distribution()
            elif choice == 7:
                self.visualize_actor_movie_count_over_time()
            elif choice == 8:
                self.visualize_top_directors_by_movie_count()  
            elif choice == 9:
                self.visualize_top_users_by_ratings()
            elif choice == 10:
                break
        
    def plot_movies_by_genre(self):
        """Fetch movie genre distribution and plot a pie chart."""
        query = "SELECT genre, COUNT(*) FROM Movies GROUP BY genre"
        self.cursor.execute(query)  
        data = self.cursor.fetchall()

        if not data:
            print(Fore.RED + "No movie data found for visualization.")
            return

        genres, counts = zip(*data)

        plt.figure(figsize=(9, 7))  
        wedges, texts, autotexts = plt.pie(
            counts, labels=genres, autopct=self.autopct_format,
            colors=['blue', 'green', 'red', 'orange'], 
            wedgeprops={'linewidth': 2, 'edgecolor': 'black'},  
            radius=1.1, pctdistance=0.75,  
            textprops={'fontsize': 12}  # Default font size for labels
        )

        # Adjust font size for 2% labels
        for text in autotexts:
            if text.get_text() == "2.0%":  
                text.set_fontsize(5)  # Set font size to 10px for 2%
            if text.get_text() == "1.0%":  
                text.set_fontsize(5)  # Set font size to 10px for 2%

        plt.title("Movies Distribution by Genre", fontsize=14, pad=20)
        plt.show()

    def plot_duration_vs_year(self):
        query = "SELECT released_year, duration FROM Movies"
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        if not data:
            print(Fore.RED + "No movie data found for visualization.")
            return

        years, durations = zip(*data)

        plt.figure(figsize=(8, 6))
        plt.scatter(years, durations, color='red', alpha=0.5)
        plt.xlabel("Release Year")
        plt.ylabel("Duration (minutes)")
        plt.title("Movie Duration vs. Release Year")
        plt.grid(True)
        plt.show()

    def plot_movie_duration_distribution(self):
        query = "SELECT duration FROM Movies"
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        if not data:
            print(Fore.RED + "No movie data found for visualization.")
            return

        durations = [d[0] for d in data]

        plt.figure(figsize=(8, 6))
        plt.hist(durations, bins=10, color='skyblue', edgecolor='black')
        plt.xlabel("Duration (minutes)")
        plt.ylabel("Number of Movies")
        plt.title("Distribution of Movie Durations")
        plt.show()

    def get_avg_ratings(self):
        """Fetch and analyze average ratings for all movies."""
        query = """
        SELECT 
            M.movie_id, 
            M.movie_name, 
            ROUND(AVG(U.rating), 1) AS avg_rating
        FROM Movies M
        JOIN User_Rating U ON M.movie_id = U.movie_id
        GROUP BY M.movie_id, M.movie_name
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        if results:
            print(Fore.WHITE + "\n📊 **Movie Ratings Analysis** 📊")
            for movie_id, movie_name, avg_rating in results:
                print(Fore.WHITE + f"🎬 {movie_name} (ID: {movie_id}) ➝ ⭐ {avg_rating}/10")
                self.analyze_movie_rating(movie_name, avg_rating)

            # Visualize the results
            self.plot_avg_ratings(results)
        else:
            print(Fore.RED + "⚠ No movie ratings found.")

    def analyze_movie_rating(self, movie_name, avg_rating):
        """Provide analysis based on the average rating."""
        if avg_rating <= 3:
            analysis = "❌ Poorly rated movie. Needs improvement."
        elif 3 < avg_rating <= 7:
            analysis = "⚠ Mixed reviews. Some liked it, some didn't."
        else:
            analysis = "✅ Highly rated! Loved by most viewers."

        print(Fore.WHITE + f"📢 Analysis for {movie_name}: {analysis}")

    def plot_avg_ratings(self, data):
        """Visualize the movie's average rating using a bar chart."""
        movie_names = [row[1] for row in data]
        avg_ratings = [float(row[2]) for row in data]  # Convert Decimal to float

        plt.figure(figsize=(8, 5))
        plt.bar(movie_names, avg_ratings, color='blue', width=0.5)
        plt.ylim(0, 10)  # Rating scale is 0-10
        plt.ylabel("Average Rating")
        plt.title("Average Ratings of Movies")
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.subplots_adjust(bottom=0.25)  # Add padding at the bottom
        
        # ✅ Convert `Decimal` to `float` before adding 0.3
        for i, v in enumerate(avg_ratings):
            plt.text(i, v + 0.3, f"", ha='center', fontsize=12, fontweight='bold')

        plt.show()

    def visualize_movies_per_actor(self):
        """Generates a bar chart showing the number of movies per actor."""
        
        query = """
        SELECT a.actor_name, COUNT(ma.movie_id) AS movie_count
        FROM Actors a
        JOIN Movie_Actor ma ON a.actor_id = ma.actor_id
        GROUP BY a.actor_name
        ORDER BY movie_count DESC
        LIMIT 10;  
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        if not results:
            print(Fore.RED + "No data available for visualization.")
            return

        actor_names = [row[0] for row in results]
        movie_counts = [row[1] for row in results]

        plt.figure(figsize=(10, 6))
        plt.barh(actor_names, movie_counts, color='skyblue')
        plt.xlabel("Number of Movies")
        plt.ylabel("Actor Name")
        plt.title("Top 10 Actors by Movie Count")
        plt.gca().invert_yaxis()

        plt.xticks(np.arange(0, max(movie_counts) + 1, 1), fontsize=10)
        plt.show()

    def visualize_actor_gender_distribution(self):
        """Generates a pie chart showing the gender distribution of actors."""
        
        query = """
        SELECT gender, COUNT(*) AS count
        FROM Actors
        GROUP BY gender;
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        if not results:
            print(Fore.RED + "No data available for visualization.")
            return

        genders = [row[0] for row in results]
        counts = [row[1] for row in results]

        plt.figure(figsize=(8, 8))
        plt.pie(counts, labels=genders, autopct="%1.1f%%", colors=['lightblue', 'lightcoral', 'lightgreen'])
        plt.title("Gender Distribution of Actors")
        plt.show()

    def visualize_top_directors_by_movie_count(self):
        """Generates a bar chart showing the top N directors by the number of movies directed."""
        
        if not self.db.conn or not self.db.conn.is_connected():
            print(Fore.RED + "Database connection is not active.")
            return

        query = f"""
        SELECT d.director_name, COUNT(md.movie_id) AS movie_count
        FROM Directors d
        JOIN movie_director md ON d.director_id = md.director_id
        GROUP BY d.director_name
        ORDER BY movie_count DESC
        LIMIT 10;
        """

        self.cursor.execute(query)
        results = self.cursor.fetchall()
        
        if not results:
            print(Fore.RED + "No data available for visualization.")
            return

        director_names = [row[0] for row in results]
        movie_counts = [row[1] for row in results]

        plt.figure(figsize=(10, 6))
        plt.barh(director_names, movie_counts, color='skyblue')
        plt.xlabel("Number of Movies")
        plt.ylabel("Director Name")
        plt.title(f"Top 10 Directors by Movie Count")
        plt.gca().invert_yaxis()
        plt.xticks(fontsize=10)
        plt.show()

    def visualize_top_users_by_ratings(self):
        """Generates a bar chart showing the top N users who rated the most movies."""

        query = f"""
        SELECT u.user_name, COUNT(ur.rating_id) AS rating_count
        FROM Users u
        JOIN User_Rating ur ON u.user_id = ur.user_id
        GROUP BY u.user_name
        ORDER BY rating_count DESC
        LIMIT 10;
        """
        
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        if not results:
            print(Fore.RED + "No data available for visualization.")
            return

        user_names = [row[0] for row in results]
        rating_counts = [row[1] for row in results]

        plt.figure(figsize=(10, 6))
        plt.barh(user_names, rating_counts, color='lightcoral')
        plt.xlabel("Number of Ratings")
        plt.ylabel("User Name")
        plt.title(f"Top 10 Users by Movie Ratings Given")
        plt.gca().invert_yaxis()
        plt.xticks(fontsize=10)
        plt.show()

    def visualize_actor_movie_count_over_time(self):
        """
        Generates a line chart showing the total number of movies featuring actors over time.
        """
        query = """
            SELECT m.released_year, COUNT(ma.movie_id) AS movie_count
            FROM Movie_Actor ma
            JOIN Movies m ON ma.movie_id = m.movie_id
            GROUP BY m.released_year
            ORDER BY m.released_year;
        """
        
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        if not results:
            print(Fore.RED + "No data available for visualization.")
            return

        years = [row[0] for row in results]
        movie_counts = [row[1] for row in results]

        plt.figure(figsize=(10, 6))
        plt.plot(years, movie_counts, marker='o', linestyle='-', color='b', label="Total Movies")
        plt.xlabel("Year")
        plt.ylabel("Number of Movies")
        plt.title("Total Actor Movie Appearances Over Time")
        plt.legend()
        plt.grid(True)
        plt.show()
