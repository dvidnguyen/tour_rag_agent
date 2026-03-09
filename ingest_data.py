import os 
from src.data_loader import TourDataLoader 
from src.vector_store import VectorStoreManager
def main(): 
    SHEET_URL = "https://docs.google.com/spreadsheets/d/15Qk8yHoRSkem1-Iz-iMcu7UzCI_h3OtZ_1x8gRGYFbY/edit?gid=0#gid=0"

    loader = TourDataLoader(SHEET_URL)

    raw_data = loader.fetch_raw_data()

    if not raw_data:
        print("Can't load data from gg sheet")
    
    docs = loader.prepare_rag_documents(raw_data)

    try:
        vector_manager = VectorStoreManager()
        vector_manager.create_and_save_db(docs)
    except Exception as e:
        print(f"Error when creating vector db: {e}")
if __name__ == "__main__":
    main()