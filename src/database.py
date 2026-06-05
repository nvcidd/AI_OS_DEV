import sqlite3


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(
            "data/ai_os.db",
            check_same_thread=False
        )

        self.cursor = self.connection.cursor()

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS tasks(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_input TEXT,

            status TEXT,

            result TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                status,
                result
            )

            VALUES(?,?,?)
            """,

            (
                user_input,
                "COMPLETED",
                str(result)
            )
        )

        self.connection.commit()

    def get_tasks(self):

        self.cursor.execute(
            "SELECT * FROM tasks"
        )

        return self.cursor.fetchall()

    def create_task(
        self,
        user_input
    ):

        self.cursor.execute(

            """
            INSERT INTO tasks(
                user_input,
                status,
                result
            )

            VALUES(?,?,?)
            """,

            (
                user_input,
                "PENDING",
                ""
            )
        )

        self.connection.commit()

        return self.cursor.lastrowid

    def update_task_status(
        self,
        task_id,
        status
    ):

        self.cursor.execute(

            """
            UPDATE tasks

            SET status=?

            WHERE id=?
            """,

            (
                status,
                task_id
            )
        )

        self.connection.commit()

    def complete_task(
        self,
        task_id,
        result
    ):

        self.cursor.execute(

            """
            UPDATE tasks

            SET
                status=?,
                result=?

            WHERE id=?
            """,

            (
                "COMPLETED",
                str(result),
                task_id
            )
        )

        self.connection.commit()

    def get_task_by_id(
        self,
        task_id
    ):

        self.cursor.execute(

            """
            SELECT *

            FROM tasks

            WHERE id=?
            """,

            (
                task_id,
            )
        )

        return self.cursor.fetchone()

    def get_total_tasks(self):

        self.cursor.execute(
            "SELECT COUNT(*) FROM tasks"
        )

        return self.cursor.fetchone()[0]

    def get_completed_tasks(self):

        self.cursor.execute(

            """
            SELECT COUNT(*)

            FROM tasks

            WHERE status='COMPLETED'
            """
        )

        return self.cursor.fetchone()[0]
    
    def fail_task(
    self,
    task_id,
    error
):

        self.cursor.execute(

            """
            UPDATE tasks

            SET
                status=?,
                result=?

            WHERE id=?
            """,

            (
                "FAILED",
                str(error),
                task_id
            )
        )

        self.connection.commit()