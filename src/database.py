import sqlite3


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(
            "ai_os.db",
            check_same_thread=False
        )

        self.cursor = self.connection.cursor()

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS tasks(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_input TEXT,

            result TEXT

        )

        """)

        self.connection.commit()


    def save_task(
        self,
        user_input,
        result
    ):

        self.cursor.execute(

            """
            INSERT INTO tasks(
                user_input,
                result
            )

            VALUES(?,?)
            """,

            (
                user_input,
                result
            )
        )

        self.connection.commit()


    def get_tasks(self):

        self.cursor.execute(
            "SELECT * FROM tasks"
        )

        return self.cursor.fetchall()