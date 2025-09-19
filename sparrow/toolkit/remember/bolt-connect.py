from neo4j import GraphDatabase

uri = "bolt://localhost:7687"  # or bolt+s:// for encryption
username = "neo4j"
password = "password"

driver = GraphDatabase.driver(uri, auth=(username, password), encrypted=False)
driver.verify_connectivity()  # Raises error if connection fails

with driver.session() as session:
    result = session.run("MATCH (n) RETURN count(n) AS node_count")
    count = result.single()["node_count"]
    print(f"Nodes in DB: {count}")