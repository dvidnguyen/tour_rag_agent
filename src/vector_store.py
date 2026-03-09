# File: src/vector_store.py
import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.config import Config

class VectorStoreManager:
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=Config.GOOGLE_API_KEY
        )
        self.db_path = Config.VECTOR_DB_DIR
        self.index_name = "tour_index"

    def create_and_save_db(self, texts):
        """Nhúng các text chunks thành vector và lưu xuống ổ cứng bằng FAISS"""
      
        
        # FAISS nhận list các texts, nhúng bằng Google Embeddings và tạo DB
        vector_db = FAISS.from_texts(texts, self.embeddings)
        
        # Tạo thư mục vector_db nếu chưa có và lưu DB xuống
        os.makedirs(self.db_path, exist_ok=True)
        vector_db.save_local(self.db_path, self.index_name)
        return vector_db

    def load_db(self):
        """Load Vector DB đã lưu từ ổ cứng lên để chuẩn bị tìm kiếm"""
        if not os.path.exists(os.path.join(self.db_path, f"{self.index_name}.faiss")):
            raise FileNotFoundError("Chưa có Vector DB. Hãy chạy file ingest_data.py trước.")
            
        return FAISS.load_local(
            self.db_path, 
            self.embeddings, 
            allow_dangerous_deserialization=True # Tham số bắt buộc của Langchain khi load FAISS cục bộ
        )