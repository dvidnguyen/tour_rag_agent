import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Cấu hình LLM
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Cấu hình RAG 
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    VECTOR_DB_DIR = "./vector_db"
    
    # Cấu hình Google Sheet (Dành cho Agent/Tool Calling)
    GOOGLE_SHEET_CRED = os.getenv("GOOGLE_SHEET_CREDENTIALS", "credentials.json")
    
    # Kiểm tra Key ngay lúc khởi động
    @staticmethod
    def validate():
        if Config.LLM_PROVIDER == "gemini" and not Config.GOOGLE_API_KEY:
            raise ValueError("LỖI: Chưa tìm thấy GOOGLE_API_KEY trong file .env")

if __name__ == "__main__":
    Config.validate()
    print(f"Provider {Config.LLM_PROVIDER}")