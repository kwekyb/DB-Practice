import sys  # 시스템 관련 기능을 사용하기 위한 모듈
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QMdiSubWindow, QToolBar, QAction, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel
# PyQt5 위젯 및 GUI 구성 요소를 가져옴
import sqlite3  # SQLite 데이터베이스를 사용하기 위한 모듈

class MainDB(QMainWindow):  # QMainWindow를 상속받아 메인 윈도우 생성
    def __init__(self):
        super().__init__()  # 부모 클래스 초기화
        self.setWindowTitle("도서 관리 시스템")  # 윈도우 제목 설정
        self.mdi = QMdiArea()  # MDI 영역 생성
        self.setCentralWidget(self.mdi)  # MDI 영역을 중앙 위젯으로 설정
        self.create_toolbar()  # 툴바 생성
        self.create_database()  # 데이터베이스 생성

    def create_toolbar(self):  # 툴바 생성 메서드
        toolbar = QToolBar("툴바")  # 툴바 생성
        self.addToolBar(toolbar)  # 메인 윈도우에 툴바 추가

        book_action = QAction("도서 테이블", self)  # 도서 테이블 액션 생성
        book_action.triggered.connect(self.open_book_table)  # 클릭 시 도서 테이블 열기
        toolbar.addAction(book_action)  # 툴바에 액션 추가

        user_action = QAction("사용자 테이블", self)  # 사용자 테이블 액션 생성
        user_action.triggered.connect(self.open_user_table)  # 클릭 시 사용자 테이블 열기
        toolbar.addAction(user_action)  # 툴바에 액션 추가

        loan_action = QAction("대출현황 테이블", self)  # 대출현황 테이블 액션 생성
        loan_action.triggered.connect(self.open_loan_table)  # 클릭 시 대출현황 테이블 열기
        toolbar.addAction(loan_action)  # 툴바에 액션 추가

    def create_database(self):  # 데이터베이스 생성 메서드
        self.conn = sqlite3.connect('library.db')  # SQLite 데이터베이스 연결
        cursor = self.conn.cursor()  # 커서 객체 생성
        # 테이블이 없으면 생성
        cursor.execute('''CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, isbn TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, contact TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS loans (id INTEGER PRIMARY KEY, status TEXT)''')
        self.conn.commit()  # 변경 사항 저장

        # 초기 데이터 추가 (테스트용)
        self.add_initial_data()  # 초기 데이터 추가 메서드 호출

    def add_initial_data(self):  # 초기 데이터 추가 메서드
        cursor = self.conn.cursor()  # 커서 객체 생성
        # books 테이블에 데이터가 없을 경우 초기 데이터 추가
        cursor.execute("SELECT COUNT(*) FROM books")
        if cursor.fetchone()[0] == 0:  # 데이터가 없으면
            cursor.execute("INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)", ("Sample Book", "Author Name", "1234567890"))
            self.conn.commit()  # 변경 사항 저장

    def open_book_table(self):  # 도서 테이블 열기 메서드
        sub_window = QMdiSubWindow()  # 서브 윈도우 생성
        sub_window.setWindowTitle("도서 테이블")  # 서브 윈도우 제목 설정
        sub_window.setMinimumSize(600, 400)  # 서브 윈도우 최소 크기 설정
        layout = QVBoxLayout()  # 레이아웃 생성

        self.book_table = QTableWidget(0, 4)  # 4열 테이블 위젯 생성
        self.book_table.setHorizontalHeaderLabels(['일련번호', '제목', '저자', 'ISBN'])  # 테이블 헤더 설정
        layout.addWidget(self.book_table)  # 테이블 위젯 레이아웃에 추가

        # 입력 상자 추가
        self.title_input = QLineEdit()  # 제목 입력 상자 생성
        self.title_input.setPlaceholderText("제목")  # 플레이스홀더 텍스트 설정
        layout.addWidget(self.title_input)  # 레이아웃에 추가

        self.author_input = QLineEdit()  # 저자 입력 상자 생성
        self.author_input.setPlaceholderText("저자")  # 플레이스홀더 텍스트 설정
        layout.addWidget(self.author_input)  # 레이아웃에 추가

        self.isbn_input = QLineEdit()  # ISBN 입력 상자 생성
        self.isbn_input.setPlaceholderText("ISBN")  # 플레이스홀더 텍스트 설정
        layout.addWidget(self.isbn_input)  # 레이아웃에 추가

        # 추가 버튼
        add_button = QPushButton("추가")  # 추가 버튼 생성
        add_button.clicked.connect(self.add_book)  # 클릭 시 add_book 메서드 호출
        layout.addWidget(add_button)  # 레이아웃에 추가

        sub_window.setLayout(layout)  # 서브 윈도우에 레이아웃 설정
        self.mdi.addSubWindow(sub_window)  # MDI 영역에 서브 윈도우 추가
        sub_window.show()  # 서브 윈도우 표시

        self.load_books()  # 도서 목록 불러오기

    def add_book(self):  # 도서 추가 메서드
        title = self.title_input.text()  # 제목 입력값 가져오기
        author = self.author_input.text()  # 저자 입력값 가져오기
        isbn = self.isbn_input.text()  # ISBN 입력값 가져오기

        if title and author and isbn:  # 모든 입력값이 있을 경우
            cursor = self.conn.cursor()  # 커서 객체 생성
            cursor.execute("INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)", (title, author, isbn))  # 데이터 삽입
            self.conn.commit()  # 변경 사항 저장
            self.load_books()  # 도서 목록 새로 고침
            self.title_input.clear()  # 제목 입력 상자 초기화
            self.author_input.clear()  # 저자 입력 상자 초기화
            self.isbn_input.clear()  # ISBN 입력 상자 초기화

    def load_books(self):  # 도서 목록 불러오기 메서드
        self.book_table.setRowCount(0)  # 기존 데이터 삭제
        cursor = self.conn.cursor()  # 커서 객체 생성
        cursor.execute("SELECT * FROM books")  # books 테이블의 모든 데이터 가져오기
        for row in cursor.fetchall():  # 가져온 데이터 반복
            row_position = self.book_table.rowCount()  # 현재 테이블 행 수 가져오기
            self.book_table.insertRow(row_position)  # 새 행 추가
            for column, data in enumerate(row):  # 열 데이터 반복
                self.book_table.setItem(row_position, column, QTableWidgetItem(str(data)))  # 테이블에 데이터 삽입

    def open_user_table(self):  # 사용자 테이블 열기 메서드
        sub_window = QMdiSubWindow()  # 서브 윈도우 생성
        sub_window.setWindowTitle("사용자 테이블")  # 서브 윈도우 제목 설정
        sub_window.setMinimumSize(600, 400)  # 서브 윈도우 최소 크기 설정
        layout = QVBoxLayout()  # 레이아웃 생성

        self.user_table = QTableWidget(0, 3)  # 3열 테이블 위젯 생성
        self.user_table.setHorizontalHeaderLabels(['일련번호', '이름', '연락처'])  # 테이블 헤더 설정
        layout.addWidget(self.user_table)  # 테이블 위젯 레이아웃에 추가

        # 입력 상자 추가
        self.user_name_input = QLineEdit()  # 이름 입력 상자 생성
        self.user_name_input.setPlaceholderText("이름")  # 플레이스홀더 텍스트 설정
        layout.addWidget(self.user_name_input)  # 레이아웃에 추가

        self.user_contact_input = QLineEdit()  # 연락처 입력 상자 생성
        self.user_contact_input.setPlaceholderText("연락처")  # 플레이스홀더 텍스트 설정
        layout.addWidget(self.user_contact_input)  # 레이아웃에 추가

        # 추가 버튼
        add_user_button = QPushButton("추가")  # 추가 버튼 생성
        add_user_button.clicked.connect(self.add_user)  # 클릭 시 add_user 메서드 호출
        layout.addWidget(add_user_button)  # 레이아웃에 추가

        sub_window.setLayout(layout)  # 서브 윈도우에 레이아웃 설정
        self.mdi.addSubWindow(sub_window)  # MDI 영역에 서브 윈도우 추가
        sub_window.show()  # 서브 윈도우 표시

    def add_user(self):  # 사용자 추가 메서드
        name = self.user_name_input.text()  # 이름 입력값 가져오기
        contact = self.user_contact_input.text()  # 연락처 입력값 가져오기

        if name and contact:  # 모든 입력값이 있을 경우
            cursor = self.conn.cursor()  # 커서 객체 생성
            cursor.execute("INSERT INTO users (name, contact) VALUES (?, ?)", (name, contact))  # 데이터 삽입
            self.conn.commit()  # 변경 사항 저장
            self.load_users()  # 사용자 목록 새로 고침
            self.user_name_input.clear()  # 이름 입력 상자 초기화
            self.user_contact_input.clear()  # 연락처 입력 상자 초기화

    def load_users(self):  # 사용자 목록 불러오기 메서드
        self.user_table.setRowCount(0)  # 기존 데이터 삭제
        cursor = self.conn.cursor()  # 커서 객체 생성
        cursor.execute("SELECT * FROM users")  # users 테이블의 모든 데이터 가져오기
        for row in cursor.fetchall():  # 가져온 데이터 반복
            row_position = self.user_table.rowCount()  # 현재 테이블 행 수 가져오기
            self.user_table.insertRow(row_position)  # 새 행 추가
            for column, data in enumerate(row):  # 열 데이터 반복
                self.user_table.setItem(row_position, column, QTableWidgetItem(str(data)))  # 테이블에 데이터 삽입

    def open_loan_table(self):  # 대출현황 테이블 열기 메서드
        sub_window = QMdiSubWindow()  # 서브 윈도우 생성
        sub_window.setWindowTitle("대출현황 테이블")  # 서브 윈도우 제목 설정
        sub_window.setMinimumSize(600, 400)  # 서브 윈도우 최소 크기 설정
        layout = QVBoxLayout()  # 레이아웃 생성

        self.loan_table = QTableWidget(0, 2)  # 2열 테이블 위젯 생성
        self.loan_table.setHorizontalHeaderLabels(['일련번호', '대출상태'])  # 테이블 헤더 설정
        layout.addWidget(self.loan_table)  # 테이블 위젯 레이아웃에 추가

        # 입력 상자 추가
        self.loan_status_input = QLineEdit()  # 대출 상태 입력 상자 생성
        self.loan_status_input.setPlaceholderText("대출 상태")  # 플레이스홀더 텍스트 설정
        layout.addWidget(self.loan_status_input)  # 레이아웃에 추가

        # 추가 버튼
        add_loan_button = QPushButton("추가")  # 추가 버튼 생성
        add_loan_button.clicked.connect(self.add_loan)  # 클릭 시 add_loan 메서드 호출
        layout.addWidget(add_loan_button)  # 레이아웃에 추가

        sub_window.setLayout(layout)  # 서브 윈도우에 레이아웃 설정
        self.mdi.addSubWindow(sub_window)  # MDI 영역에 서브 윈도우 추가
        sub_window.show()  # 서브 윈도우 표시

    def add_loan(self):  # 대출 추가 메서드
        status = self.loan_status_input.text()  # 대출 상태 입력값 가져오기

        if status:  # 입력값이 있을 경우
            cursor = self.conn.cursor()  # 커서 객체 생성
            cursor.execute("INSERT INTO loans (status) VALUES (?)", (status,))  # 데이터 삽입
            self.conn.commit()  # 변경 사항 저장
            self.load_loans()  # 대출 목록 새로 고침
            self.loan_status_input.clear()  # 대출 상태 입력 상자 초기화

    def load_loans(self):  # 대출 목록 불러오기 메서드
        self.loan_table.setRowCount(0)  # 기존 데이터 삭제
        cursor = self.conn.cursor()  # 커서 객체 생성
        cursor.execute("SELECT * FROM loans")  # loans 테이블의 모든 데이터 가져오기
        for row in cursor.fetchall():  # 가져온 데이터 반복
            row_position = self.loan_table.rowCount()  # 현재 테이블 행 수 가져오기
            self.loan_table.insertRow(row_position)  # 새 행 추가
            for column, data in enumerate(row):  # 열 데이터 반복
                self.loan_table.setItem(row_position, column, QTableWidgetItem(str(data)))  # 테이블에 데이터 삽입

if __name__ == "__main__":  # 메인 실행 부분
    app = QApplication(sys.argv)  # QApplication 객체 생성
    main_db = MainDB()  # MainDB 객체 생성
    main_db.show()  # 메인 윈도우 표시
    sys.exit(app.exec_())  # 애플리케이션 실행 및 종료
