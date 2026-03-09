# File: src/data_loader.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from src.config import Config

class TourDataLoader:
    def __init__(self, sheet_name_or_url):
        """
        Khởi tạo kết nối với Google Sheets API
        """
        self.sheet_identifier = sheet_name_or_url
        print("Đang xác thực với Google Sheets bằng credentials.json...")
        
        # Định nghĩa các quyền (scopes) cần thiết để truy cập Google Sheets và Drive
        scopes = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        

        creds = ServiceAccountCredentials.from_json_keyfile_name(Config.GOOGLE_SHEET_CRED, scopes)
        self.client = gspread.authorize(creds)
        # Authentication with Google Sheets successful
    def fetch_raw_data(self):
        """Lấy dữ liệu thô dạng danh sách các Dictionary từ Sheet"""
        try:
            # Nếu bạn truyền vào URL thì dùng open_by_url, nếu truyền tên file thì dùng open
            if "http" in self.sheet_identifier:
                sheet = self.client.open_by_url(self.sheet_identifier).sheet1
            else:
                sheet = self.client.open(self.sheet_identifier).sheet1
            # Get all record from sheet 
            records = sheet.get_all_records()

            return records
        except Exception as e:
            print(f" Lỗi khi đọc Google Sheet: {e}")
            return []

    def prepare_rag_documents(self, raw_records):
        """
        HÀM QUAN TRỌNG NHẤT: Biến đổi từng dòng (Row) thành một đoạn văn bản (Text Chunk)
        để Vector DB có thể hiểu được ngữ nghĩa.
        """
        documents = []
        for row in raw_records:
            if not row.get("Mã Tour"): 
                continue
                
            # Ghép nối các cột thành một đoạn văn bản có cấu trúc tự nhiên
            text_chunk = (
                f"Thông tin Tour mã {row.get('Mã Tour', 'N/A')}: "
                f"Tên tour là '{row.get('Tên Tour', 'N/A')}', tổ chức tại {row.get('Địa Điểm', 'N/A')}. "
                f"Lịch trình kéo dài {row.get('Thời Gian', 'N/A')} với mức giá {row.get('Giá Tiền (VNĐ)', 'N/A')} VNĐ/người. "
                f"Khách hàng sẽ lưu trú tại {row.get('Hạng Khách Sạn', 'N/A')}, loại phòng {row.get('Loại Phòng/Giường', 'N/A')}. "
                f"Điểm nhấn của tour: {row.get('Điểm Nhấn / Lịch Trình Tóm Tắt', 'N/A')}. "
                f"Đánh giá từ khách hàng: {row.get('Đánh Giá', 'N/A')} sao. "
                f"Tình trạng hiện tại: {row.get('Tình Trạng', 'N/A')}."
            )
            documents.append(text_chunk)
            
        return documents

if __name__ == "__main__":
   
    SHEET_URL = "ĐIỀN_LINK_GOOGLE_SHhttps://docs.google.com/spreadsheets/d/15Qk8yHoRSkem1-Iz-iMcu7UzCI_h3OtZ_1x8gRGYFbY/edit?gid=0#gid=0EET_CỦA_BẠN_VÀO_ĐÂY" 
    
    loader = TourDataLoader(SHEET_URL)
    raw_data = loader.fetch_raw_data()
    
    if raw_data:
        docs = loader.prepare_rag_documents(raw_data)
        print("\n--- TEST KẾT QUẢ DỮ LIỆU ĐÃ XỬ LÝ CHO RAG (1 Chunk đầu tiên) ---")
        print(docs[0])