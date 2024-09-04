import pandas as pd
import chromadb
import uuid


class Portfolio:
    def __init__(self, csv_file="app/resource/my_portfolio.csv"):
        self.csv_file = csv_file
        self.portfolio_data = pd.read_csv(csv_file)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.portfolio_collection = self.chroma_client.get_or_create_collection(name="tech_portfolio")

    def initialize_portfolio(self):
        if not self.portfolio_collection.count():
            for _, entry in self.portfolio_data.iterrows():
                self.portfolio_collection.add(
                    documents=entry["Techstack"],
                    metadatas={"links": entry["Links"]},
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills_list):
        query_result = self.portfolio_collection.query(query_texts=skills_list, n_results=2)
        return query_result.get('metadatas', [])



