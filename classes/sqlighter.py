from importlib.util import set_loader
import sqlite3
import data

class SQLighter:

    def __init__(self, database_file):
        """Connecting db and saving connection cursor"""
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()
    
    def get_users(self, sub_status = True):
        """Getting all bot users"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `users` WHERE `sub_status` = ?", (sub_status,)).fetchall()

    def user_exists(self, user_id):
        """Checking - user already exists in db or not"""
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))
    
    def add_user(self, user_id, user_name, sub_status = True):
        """Adding user in db"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`, `user_name`, `sub_status`) VALUES (?, ?, ?)", (user_id, user_name, sub_status))
    
    def update_subscribe(self, user_id, sub_status):
        """Updating subscription status"""
        return self.cursor.execute("UPDATE `users` SET `sub_status` = ? WHERE `user_id` = ?", (user_id, sub_status))
    
    def close(self):
        """Close db connection"""
        self.connection.close()