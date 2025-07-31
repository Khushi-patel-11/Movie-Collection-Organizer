from Movie_Collection import MovieCollection
from tabulate import tabulate
import re
from colorama import init, Fore, Style

init(autoreset=True)

class UserManagement(MovieCollection):
        
    def manage_users(self):
        while True:
            options = [
                "Add User 🆕",
                "Update User ✏️",
                "Remove User ❌",
                "List Users 📋",
                "Rate Movies ⭐",
                "Back 🔙"
            ]
            self.display_menu("User Management", options)
            choice = self.get_user_choice(options)
            if choice == 1:
                self.add_user()
            elif choice == 2:
                self.update_user()
            elif choice == 3:
                self.remove_user()
            elif choice == 4:
                self.list_users()
            elif choice == 5:
                self.add_user_rating_to_movie()
            elif choice == 6:
                break

    def add_user(self, user_name=None):
        """Add a new user to the database and return user_id. If user exists, return existing user_id."""
        try:
            if user_name is None:
                user_name = input(Fore.GREEN + "Enter user's name: ").strip()

            for user_id, user_info in self.users.items():
                if user_info["user_name"].lower() == user_name.lower():
                    print(Fore.RED + f"User '{user_name}' already exists.")
                    return user_id

            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            while True:
                user_email = input(Fore.GREEN + "Enter user's email: ").strip()
                if re.match(email_pattern, user_email):
                    break
                print(Fore.RED + "Invalid email format. Please enter a valid email.")

            for user_id, user_info in self.users.items():
                if user_info["user_email"].lower() == user_email.lower():
                    print(Fore.RED + f"User with email '{user_email}' already exists.")
                    return user_id

            password = input(Fore.GREEN + "Enter password: ").strip()

            query = "INSERT INTO Users (user_name, user_email, password) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (user_name, user_email, password))
            self.db.conn.commit()

            user_id = self.cursor.lastrowid

            self.users[user_id] = {
                "user_name": user_name,
                "user_email": user_email,
                "password": password
            }

            print(Fore.WHITE + f"User '{user_name}' added successfully.")
            return user_id

        except Exception as e:
            print(Fore.RED + f"Error adding user: {e}")
            return None

    def update_user(self):
        """Prompts the user for a name and updates their email and password if they exist."""
        user_name = input(Fore.GREEN + "Enter user name to update: ").strip()
        
        user_id = None
        for id_, user in self.users.items():
            if user["user_name"].lower() == user_name.lower():
                user_id = id_
                break

        if user_id is None:
            print(Fore.RED + "User not found.")
            return

        print(Fore.YELLOW + '(Leave blank to keep unchanged):')
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        while True:
            new_email = input(Fore.GREEN + "Enter new email: ").strip()
            if not new_email:
                new_email = self.users[user_id]["user_email"]
                break
            if re.match(email_pattern, new_email):
                break
            print(Fore.RED + "Invalid email format. Please enter a valid email.")
        
        new_password = input(Fore.GREEN + "Enter new password: ").strip()
        
        update_fields = []
        update_values = []

        if new_email:
            update_fields.append("user_email = %s")
            update_values.append(new_email)
        if new_password:
            update_fields.append("password = %s")
            update_values.append(new_password)

        if not update_fields:
            print(Fore.RED + "No valid fields to update.")
            return

        update_values.append(user_id)
        query = f"UPDATE Users SET {', '.join(update_fields)} WHERE user_id = %s"

        try:
            self.cursor.execute(query, update_values)
            self.db.conn.commit()

            self.users[user_id]["user_email"] = new_email
            if new_password:
                self.users[user_id]["password"] = new_password

            print(Fore.WHITE + "User updated successfully.")
        except mysql.connector.Error as err:
            print(Fore.RED + "Error:", err)
    
    def remove_user(self):
        """Remove a user by name from the database and the in-memory users dictionary."""
        try:
            if not self.users:
                print(Fore.RED + "No users available to remove.")
                return

            user_name = input(Fore.GREEN + "Enter the name of the user to remove: ").strip()

            user_id = None
            for key, user_info in self.users.items():
                if user_info['user_name'].lower() == user_name.lower():
                    user_id = key
                    break

            if user_id is None:
                print(Fore.RED + f"User '{user_name}' not found.")
                return

            query = "DELETE FROM Users WHERE user_id = %s"
            self.cursor.execute(query, (user_id,))
            self.db.conn.commit()

            removed_user = self.users.pop(user_id)

            print(Fore.WHITE + f"User '{removed_user['user_name']}' has been successfully removed.")
        except Exception as e:
            print(Fore.RED + f"Error removing user: {e}")

    def list_users(self):
        """Displays all users' information except user_id using self.users."""
        if not self.users:
            print(Fore.RED + "No users found in memory.")
            return

        table_data = [
            [user["user_name"], user["user_email"], user["password"]]
            for user in self.users.values()
        ]

        headers = ["User Name", "Email", "Password"]

        print(Fore.WHITE + tabulate(table_data, headers=headers, tablefmt="grid"))