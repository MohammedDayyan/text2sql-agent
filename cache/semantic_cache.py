import os
import json
import numpy as np

CACHE_PATH = "cache/semantic_cache.json"

def load_semantic_cache():
    if not os.path.exists(CACHE_PATH):
        return [], []

    with open(CACHE_PATH, "r") as f:
        data = json.load(f)
        questions = [item["question"] for item in data]
        sqls = [item["sql"] for item in data]
        return questions, sqls


def save_semantic_cache(questions, sqls):
    data = []
    for q, s in zip(questions, sqls):
        data.append({"question": q, "sql": s})

    with open(CACHE_PATH, "w") as f:
        json.dump(data, f, indent=4)


def build_faiss_index(questions):
    if len(questions) == 0:
        return None

    embeddings = model.encode(questions)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    faiss.write_index(index, INDEX_PATH)
    return index


def load_index(questions):
    if os.path.exists(INDEX_PATH):
        return faiss.read_index(INDEX_PATH)
    return build_faiss_index(questions)


def get_semantic_sql(question, threshold=0.85):
    questions, sqls = load_semantic_cache()

    if len(questions) == 0:
        return None

    #index = load_index(questions)
    store_embeds = model.encode(questions)
    q_embed = model.encode([question])[0]
    similarities = store_embeds @ q_embed / (
        np.linalg.norm(store_embeds,axis=1) * np.linalg.norm(q_embed)
    )
    #distances, indices = index.search(np.array(q_embed), k=1)
    
    best_match_idx = np.argmax(similarities)
    best_score = similarities[best_match_idx]

    print("Semantic similarity score:", best_score)
    
    #similarity = 1 / (1 + distances[0][0])  # convert L2 → similarity

    if best_score >= threshold:
        return sqls[best_match_idx]

    return None


def store_semantic_sql(question, sql):
    questions, sqls = load_semantic_cache()

    questions.append(question)
    sqls.append(sql)

    save_semantic_cache(questions, sqls)
    build_faiss_index(questions)

