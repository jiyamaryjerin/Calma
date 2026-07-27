import chromadb
from sentence_transformers import SentenceTransformer


class VectorMemoryService:

    def __init__(self):

        print("Loading Embedding Model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Embedding Model Loaded!")

        self.client = chromadb.PersistentClient(
            path="database"
        )

        self.collection = self.client.get_or_create_collection(
            name="calma_memories"
        )

    def add_memory(self, memory):

        embedding = self.model.encode(
            memory.fact
        ).tolist()

        self.collection.add(
            ids=[str(memory.timestamp)],
            documents=[memory.fact],
            embeddings=[embedding],
            metadatas=[
                {
                    "type": memory.type,
                    "importance": memory.importance,
                }
            ],
        )

    def search(self, query, n_results=3):

        embedding = self.model.encode(
            query
        ).tolist()

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=n_results,
        )

        return results

    def search_excluding_exact_match(self, query, n_results=3):
        """
        Search for memories while excluding exact text matches.
        Useful to skip the current message and get previous related memories.
        """

        embedding = self.model.encode(
            query
        ).tolist()

        # Get more results to filter duplicates
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=n_results + 2,
        )

        # Filter out exact matches
        filtered_documents = []
        filtered_ids = []
        filtered_distances = []
        filtered_metadatas = []

        for i, doc in enumerate(results["documents"][0]):
            if doc.strip() != query.strip():
                filtered_documents.append(doc)
                filtered_ids.append(results["ids"][0][i])
                if results["distances"]:
                    filtered_distances.append(results["distances"][0][i])
                if results["metadatas"]:
                    filtered_metadatas.append(results["metadatas"][0][i])

        # Return only n_results
        return {
            "documents": [filtered_documents[:n_results]],
            "ids": [filtered_ids[:n_results]],
            "distances": [filtered_distances[:n_results]] if filtered_distances else [],
            "metadatas": [filtered_metadatas[:n_results]] if filtered_metadatas else [],
        }

    def clear(self):
        """
        Removes all memories from the ChromaDB collection.
        """

        data = self.collection.get()

        if data["ids"]:
            self.collection.delete(ids=data["ids"])

        print("Vector memory cleared.")


vector_memory_service = VectorMemoryService()