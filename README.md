# Movie-Collection-Organizer

A comprehensive Python application for managing and visualizing a movie collection, including actors, directors, users, and ratings. The project uses a MySQL database for persistent storage and provides features for CRUD operations, reporting, and data visualization.

## Features

- **Movie Management:** Add, update, remove, list movies; assign actors and directors; manage ratings.
- **Actor & Director Management:** Add, update, remove, list actors/directors; associate them with movies.
- **User Management:** Add, update, remove, list users; allow users to rate movies.
- **Reporting:** Generate CSV and PDF reports for movies, actors, directors, and ratings.
- **Visualization:** Visualize data with bar charts, pie charts, histograms, and scatter plots using Matplotlib and Seaborn.
- **Database Integration:** Uses MySQL for data storage (see [Tables.py](Tables.py) for schema).
- **Command-Line Interface:** Interactive menus for all management and visualization tasks.

## Project Structure

```
Actor_Management.py
Director_Management.py
Movie_Collection.py
Movie_Management.py
MovieCollectionController.py
User_Management.py
Visualization.py
reports.py
Tables.py
Lagaan_directors.pdf
```

## Database Setup

1. Install MySQL and create a database named `movie`.
2. Use the table definitions in [Tables.py](Tables.py) to create the required tables.
3. Update the database credentials in the code if needed (default user: `root`, password: prompted at runtime).

## Requirements

- Python 3.8+
- MySQL server
- Required Python packages:
  - `mysql-connector-python`
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `tabulate`
  - `colorama`
  - `reportlab`
  - `fpdf` (for some PDF exports)

Install dependencies using:
```sh
pip install mysql-connector-python pandas matplotlib seaborn tabulate colorama reportlab fpdf
```

## Usage

1. Start the application:
   ```sh
   python MovieCollectionController.py
   ```
2. Follow the interactive menu to manage movies, actors, directors, users, generate reports, and visualize data.

## Reports & Visualization

- Reports can be generated as CSV and PDF files.
- Visualizations include genre distribution, ratings, actor/director statistics, and more.

## Notes

- All database credentials are prompted securely at runtime.
- The application uses in-memory dictionaries for fast access, synced with the database.
- For any schema changes, update [Tables.py](Tables.py) and re-run the table creation scripts.

## License

This project is for educational purposes.

---

**Author:** Khushi Patel  
