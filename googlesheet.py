import gspread
from oauth2client.service_account import ServiceAccountCredentials

def insert_row(date:str, time:str, price:str, updown:str, percent:str):
    # 1. 인증 및 클라이언트 생성
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    # "credentials.json"을 실제 다운로드한 서비스 계정 키 파일 경로로 변경하세요.
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    # 2. 공유된 구글 시트 열기
    # "SpreadsheetName"을 구글 시트의 제목으로, "SheetName"을 작업하려는 시트 이름으로 변경하세요.
    spreadsheet = client.open("환율정보")
    worksheet = spreadsheet.worksheet("엔화")

    existing_rows = worksheet.col_values(1)  # 첫 번째 열(A열)의 값들을 가져옴
    next_available_row = len(existing_rows) + 1  # 데이터가 채워진 마지막 행 다음 행

    new_row_data = [date, time, price, updown, percent]
    worksheet.insert_row(new_row_data, index=next_available_row)