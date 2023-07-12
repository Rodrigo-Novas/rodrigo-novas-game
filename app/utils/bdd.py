"""Bdd module."""

import sqlite3


class Connection:
    def create_table(self):
        """
        The function creates a table named "player" in a SQLite database named "game.db" with three columns:
        id (integer primary key autoincrement), player_name (text), and score (real).
        """
        conexion = sqlite3.connect("game.db")
        try:
            conexion.execute(
                """create table player (
                                    id integer primary key autoincrement,
                                    player_name text,
                                    score real
                                )"""
            )
        except sqlite3.OperationalError:
            print("La tabla player ya existe")
        finally:
            conexion.close()

    def insert_data(self, player_name, score):
        """
        The function `insert_data` inserts a player's name and score into a SQLite database.

        Args:
          player_name: The player's name that you want to insert into the database.
          score: The "score" parameter represents the score achieved by the player. It is a numerical value
        that indicates the player's performance in the game.
        """
        conexion = sqlite3.connect("game.db")
        try:
            conexion.execute("insert into player(player_name,score) values (?,?)", (player_name, score))
            conexion.commit()
        except sqlite3.OperationalError:
            print("No se pudo insertar")
        finally:
            conexion.close()

    def get_last_one(self):
        """
        The function retrieves the last row from the "player" table in a SQLite database named "game.db".

        Returns:
          the last row from the "player" table in the "game.db" database.
        """
        conexion = sqlite3.connect("game.db")
        try:
            cursor = conexion.execute("SELECT * FROM player ORDER BY id DESC LIMIT 1")
            fila = cursor.fetchone()
            return fila
        except Exception as e:
            print(e)
        finally:
            conexion.close()

    def get_last_user_order_by_score(self, user):
        """
        The function retrieves the last order made by a user from a SQLite database, ordered by score in
        descending order.

        Args:
          user: The "user" parameter is the name of the player for whom you want to retrieve the last order
        by score.

        Returns:
          the last user order by score from the "player" table in the "game.db" database.
        """
        conexion = sqlite3.connect("game.db")
        try:
            cursor = conexion.execute(
                "SELECT * FROM player WHERE (player_name=:puser OR :puser='') ORDER BY score DESC LIMIT 1", {"puser": user}
            )
            fila = cursor.fetchone()
            return fila
        except Exception as e:
            print(e)
        finally:
            conexion.close()

    def get_top_ten_score(self):
        """
        The function retrieves the top ten scores from a SQLite database table named "player" and returns
        the result as a list of rows.

        Returns:
          the top ten scores from the "player" table in the "game.db" database.
        """
        conexion = sqlite3.connect("game.db")
        try:
            cursor = conexion.execute("SELECT * FROM player ORDER BY score DESC LIMIT 10")
            fila = cursor.fetchall()
            return fila
        except Exception as e:
            print(e)
        finally:
            conexion.close()
