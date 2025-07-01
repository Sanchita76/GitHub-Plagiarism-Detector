import openai, os, numpy as np

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embedding(text):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def compute_similarity_score(path1, path2):
    def read_code(path):
        code = ""
        for root, _, files in os.walk(path):
            for f in files:
                if f.endswith(".py"):
                    with open(os.path.join(root, f)) as file:
                        code += file.read()
        return code

    emb1 = np.array(get_embedding(read_code(path1)))
    emb2 = np.array(get_embedding(read_code(path2)))
    sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    return round(sim, 4), round(sim * 100, 2)