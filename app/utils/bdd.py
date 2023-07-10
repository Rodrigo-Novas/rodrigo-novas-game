"""Bdd module."""

import sqlite3


class Connection:
    def create_table(self):
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
        conexion = sqlite3.connect("game.db")
        try:
            conexion.execute("insert into player(player_name,score) values (?,?)", (player_name, score))
            conexion.commit()
        except sqlite3.OperationalError:
            print("No se pudo insertar")
        finally:
            conexion.close()

    def get_last_one(self):
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
        conexion = sqlite3.connect("game.db")
        try:
            cursor = conexion.execute("SELECT * FROM player ORDER BY score DESC LIMIT 10")
            fila = cursor.fetchall()
            return fila
        except Exception as e:
            print(e)
        finally:
            conexion.close()
