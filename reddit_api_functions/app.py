import psycopg2
from config import config
import random

def connect():
    connection = None
    rand_numb = random.randint(1, 3326)
    try:
        params = config()

        print("Connecting...")

        connection = psycopg2.connect(**params)
        cur = connection.cursor()

        print("Random number: {} ".format(rand_numb))
        query = '''SELECT media FROM "MEME"."meme_db" WHERE key={};'''.format(rand_numb)
        cur.execute(query)

        db_version = cur.fetchall()
        print(db_version)

        cur.close()
        print("Connected to the database")

    except psycopg2.Error as e:
        print("Error connecting to the database:", e)

    finally:
        if connection is not None:
            connection.close()
            print("Connection closed")


if __name__ == "__main__":

    connect()