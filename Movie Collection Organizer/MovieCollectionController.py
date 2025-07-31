from Actor_Management import ActorManagement
from Movie_Management import MovieManagement
from Director_Management import DirectorManagement
from User_Management import UserManagement
from Visualization import Visualization
from abc import abstractmethod
from colorama import init, Fore, Style

init(autoreset=True)

class MovieCollectionController(MovieManagement,ActorManagement,DirectorManagement,UserManagement,Visualization):
    

    

    def main_menu(self):
        options = [
            "Movie Management",
            "Actor Management",
            "Director Management",
            "User Management",
            "Generate Reports",
            "Exit"
        ]
        
        while True:
            self.display_menu("Main", options)
            choice = self.get_user_choice(options)
            if choice == 1:
                self.manage_movies()
            elif choice == 2:   
                self.manage_actors()
            elif choice == 3:
                self.manage_directors()
            elif choice == 4:
                self.manage_users()
            elif choice == 5:
                self.visualization()
            elif choice == 6: 
                if hasattr(self, 'db') and self.db is not None:
                    self.db.close()
                    del self.db
                print(Fore.WHITE + "Exiting the application. Goodbye!")
                break
            else:
                print(Fore.RED + "Invalid choice, please try again.")
                
if __name__ == "__main__":
    controller = MovieCollectionController()
    controller.main_menu()
