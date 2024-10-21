import tqdm
import psycopg2
from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
conn = psycopg2.connect(
    database="signs",
    host="localhost",
    user="postgres",
    port=5432,
)
register_vector(conn)
cur = conn.cursor()

cur.execute("SELECT word FROM signs")
words = cur.fetchall()
words = [word[0] for word in words]
bar = tqdm.tqdm(total=len(words))
for word in words:
    embedding = model.encode(word)
    cur.execute("UPDATE signs SET embedding = %s WHERE word = %s", (embedding, word))
    conn.commit()

    bar.update(1)
