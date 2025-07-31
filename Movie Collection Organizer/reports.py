import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

def generate_movie_report():
    """Generates a movie collection report and saves it as a CSV and PDF file."""
    
    try:
        # Connect to MySQL Database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vraj",
            database="movie"
        )
        cursor = db.cursor()

        # Fetch movie details with ratings
        query = """
        SELECT m.movie_name, m.released_year, m.genre, m.duration, 
               d.director_name, 
               COALESCE(AVG(r.rating), 0) AS avg_rating
        FROM Movies m
        LEFT JOIN movie_director md ON m.movie_id = md.movie_id
        LEFT JOIN Directors d ON md.director_id = d.director_id
        LEFT JOIN User_Rating r ON m.movie_id = r.movie_id
        GROUP BY m.movie_id, d.director_name
        ORDER BY m.released_year DESC;
        """ 

        cursor.execute(query)
        results = cursor.fetchall()

        # Convert to DataFrame
        df = pd.DataFrame(results, columns=["Movie Name", "Year", "Genre", "Duration (min)", "Director", "Avg Rating"])
        print(df)

        # Save as CSV
        df.to_csv("movie_collection_report.csv", index=False)
        print("Report saved as movie_collection_report.csv")

        # Save as PDF
        save_report_as_pdf(df, "movie_collection_report.pdf")

        # Close database connection
        cursor.close()
        db.close()

    except Exception as e:
        print(f"Error generating report: {e}")

def save_report_as_pdf(df, filename="movie_collection_report.pdf"):
    """Saves the report as a PDF file."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

    plt.savefig(filename, format="pdf", bbox_inches="tight")
    print(f"Report saved as {filename}")

# Generate the report
generate_movie_report()
save_report_as_pdf()