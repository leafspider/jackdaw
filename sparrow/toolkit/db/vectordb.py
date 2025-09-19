import psycopg2, psycopg2.extras, random, uuid, logging, asyncio
from psycopg2.extensions import connection
import numpy as np
import os

psycopg2.extras.register_uuid()

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class PostgresDb:

    def __init__(self, db_config=None):

        self.db_config: dict = db_config
        self.conn: connection = None

    def connect(self):

        if self.db_config is None:
            self.db_config = {
                "user": os.environ['POSTGRES_USER'],
                "password": os.environ['POSTGRES_PASSWORD'],
                "host": os.environ['POSTGRES_HOST'],
                "database": os.environ['POSTGRES_DBNAME'],
                "port": os.environ['POSTGRES_PORT'],
            }

        if self.conn is None:
            try:
                with psycopg2.connect(**self.db_config) as conn:
                    self.conn = conn
                    log.info(
                        print("Connected to Postgres at " + self.db_config["host"])
                    )

            except (psycopg2.DatabaseError, Exception) as error:
                log.info(error)
                print(error)

        return self.conn

    def disconnect(self):

        self.conn.close()
        log.info(print("Disconnected from Postgres at " + self.db_config["host"]))
                
    def execute(self, sql):

        ret = None
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    ret = cur.statusmessage
                conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            log.info(print(error))
        finally:
            return ret
        
    def add_primary_key(self, table, column):

        sql: str = f"""ALTER TABLE {table}
                    ADD PRIMARY KEY({column});"""        
        return self.execute(sql)

    def create_unique_index(self, table, column):

        sql = f"""CREATE UNIQUE INDEX IF NOT EXISTS {table.replace('.','_')}_{column}_idx 
                    ON {table} ({column});"""
        return self.execute(sql)
    
    def add_unique_constraint(self, table, column):

        sql: str = f"""ALTER TABLE {table} 
                    DROP CONSTRAINT IF EXISTS unique_{column};         
                  ALTER TABLE {table} 
                    ADD CONSTRAINT unique_{column} 
                    UNIQUE USING INDEX {table.replace('.','_')}_{column}_idx;"""        
        return self.execute(sql)
        
    def insert(self, table, **kwargs):

        keys = ", ".join(key for key in kwargs.keys())
        values = ", ".join("'" + str(value).replace("'", "''") + "'" for value in kwargs.values())
        
        sql: str = f"""INSERT INTO {table} ({keys}) VALUES ({values}) RETURNING id;"""

        ret = None
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    rows = cur.fetchone()
                    if rows:
                        ret = rows[0]
                conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            log.info(print(error))
        finally:
            return ret
    
    def update(self, id, table, **kwargs):

        keys_values = ", ".join(key +"='"+ str(value).replace("'", "''") + "'" for key, value in kwargs.items())

        sql: str = f""" UPDATE {table} SET {keys_values} WHERE id = '{id}'"""
      
        return self.execute(sql)
    
    def delete(self, id, table):

        sql: str = f"""DELETE FROM {table} WHERE id='{id}'"""
        return self.execute(sql)    

    def select(self, id, table, columns):
        
        keys = ', '.join(column for column in columns)

        sql: str = f"""SELECT {keys} FROM {table} WHERE id = %s"""
        
        rows = None

        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (id,))
                    rows = cur.fetchall()
                conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            log.info(print(error))
        finally:
            return rows


class VectorDb(PostgresDb):

    table = 'blocks'
    vector_column = 'embedding'
    text_column = 'text'
    
    def insert(self, table=table, **kwargs):
        return super().insert(table, **kwargs)
        
    def update(self, id, table=table, **kwargs):
        return super().update(id, table, **kwargs)
                     
    def delete(self, id, table=table):
        return super().delete(id, table)

    def create_embedding_index(self, table=table, column=vector_column):
        sql: str = f"""CREATE INDEX IF NOT EXISTS {table.replace('.','_')}_{column}_idx 
                    ON {table} 
                    USING hnsw ({column} vector_cosine_ops);"""
        return self.execute(sql)
    
    def fetch_embedding(self, id, table=table, column=vector_column):
        sql: str = f"""SELECT {column}
                FROM {table} 
                WHERE id = %s"""        
        vector = None
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (id,))
                    vector = np.array(np.matrix(cur.fetchone()[0])).ravel().tolist()    # TODO fixup conversion 
                conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            log.info(print(error))
        finally:
            return vector

    def fetch_text(self, id, table=table, column=text_column):        
        return super().select(id, table, {column})[0][0]

    def search_by_id(self, id, num_results=10, table=table, column=vector_column):
        vector = self.fetch_embedding(id, table, column)
        return self.search_by_embedding(vector, num_results, table, column)

    def search_by_embedding(self, vector: list, num_results=10, table=table, column=vector_column):
        sql: str = f"""SELECT id, {column} <=> '{vector}' as similarity 
                FROM {table} 
                ORDER BY {column} <=> '{vector}' DESC LIMIT {num_results}"""
        rows = {}
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    rows = cur.fetchall()
                conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            log.info(print(error))
        finally:
            return rows
        
    # def fetch_results_json(s, query, num_results=10):

    #     fetch_results = s.fetch_results(query, num_results)
    #     data = {"query": query, "follow_up_questions": "None", "answer": "None", "images": "None", "results": []}
    #     data_results = []
    #     for res in fetch_results:
    #         data_results.append({"title": res.title, "url": res.url, "content": res.description})
    #     data["results"] = data_results
    #     return data


if __name__ == "__main__":

    from tests.toolkit.test_vectordb_with_embedder import test_embedder_with_local_vector_db

    asyncio.run(test_embedder_with_local_vector_db())
