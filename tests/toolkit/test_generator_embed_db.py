import random, uuid, asyncio, pytest
import psycopg2, psycopg2.extras
from psycopg2.extensions import connection
from sparrow.toolkit.db.vectordb import VectorDb
import config, logging
from typing import List
from sparrow.toolkit.embed.embedder import Embedder
from sparrow.toolkit.generate.tweet_generator import TweetGenerator


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

psycopg2.extras.register_uuid()


async def test_generator_embed_db():

    db_config = {
        "user": config.POSTGRES_USER,
        "password": config.POSTGRES_PASSWORD,
        "host": config.POSTGRES_HOST,
        "database": config.POSTGRES_DBNAME,
        "port": config.POSTGRES_PORT,
    }

    db = VectorDb(db_config)

    db.connect()
    assert isinstance(db.conn, connection)

    embedder = Embedder()

    # text1 = """Question from a Trad beginner. What's the methodology for climbing Trad routes that have no anchors in areas where slinging trees is prohibited. For example, the climbs Larry and Curly at Old Baldy. Are people building gear anchors at the top of the climb and then cleaning the route, disassembling the anchor, and walking off? If there are no features other than trees on the top of the cliff it seems like disassembling the anchor would be difficult and dangerous, and I cannot imagine doing this. Apologies if I am missing some obvious here."""

    gen = TweetGenerator()

    text1 = gen.generate_text("artificial intelligence")
    print(text1)

    vector1 = await embedder.create_embedding(text1)
    assert len(vector1) > 0
    assert isinstance(vector1, List)
    assert isinstance(vector1[0], float)

    doc_id1 = db.insert(
        text=text1, 
        embedding=vector1
    )
    assert isinstance(doc_id1 , uuid.UUID )

    # vector1 = db.fetch_embedding(doc_id1)
    # assert len(vector1) > 0
    # assert isinstance(vector1, List)
    # assert isinstance(vector1[0], float)

    # rows = db.search_by_embedding(vector1, num_results=3)
    # assert len(rows) < 4
    # for row in rows:
    #     assert isinstance(row[0], uuid.UUID)
    #     assert isinstance(row[1], float)

    # num_results = 100
    # rows = db.search_by_id(doc_id1, num_results)
    # assert len(rows) < num_results + 1
    # for row in rows:
    #     assert isinstance(row[0], uuid.UUID)
    #     assert isinstance(row[1], float)

    # for row in rows:
    #     id = row[0]
    #     text = db.fetch_text(id)[:50]
    #     print(text)

    # assert db.delete(doc_id1) == "DELETE 1"

    db.disconnect()


if __name__ == '__main__':

    asyncio.run(test_generator_embed_db())

