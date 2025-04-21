import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QMdiSubWindow, QToolBar, QAction, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel
import sqlite3

class MainDB(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("도서 관리 시스템")
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        self.create_toolbar()
        self.create_database()

    def create_toolbar(self):
        toolbar = QToolBar("툴바")
        self.addToolBar(toolbar)

        book_action = QAction("도서 테이블", self)
        book_action.triggered.connect(self.open_book_table)
        toolbar.addAction(book_action)

        user_action = QAction("사용자 테이블", self)
        user_action.triggered.connect(self.open_user_table)
        toolbar.addAction(user_action)

        loan_action = QAction("대출현황 테이블", self)
        loan_action.triggered.connect(self.open_loan_table)
        toolbar.addAction(loan_action)

    def create_database(self):
        self.conn = sqlite3.connect('library.db')
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, isbn TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, contact TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS loans (id INTEGER PRIMARY KEY, status TEXT)''')
        self.conn.commit()

        # 초기 데이터 추가 (테스트용)
        self.add_initial_data()

    def add_initial_data(self):
        cursor = self.conn.cursor()
        # 기존 데이터가 없을 경우에만 초기 데이터 추가
        cursor.execute("SELECT COUNT(*) FROM books")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)", ("Sample Book", "Author Name", "1234567890"))
            self.conn.commit()

    def open_book_table(self):
        sub_window = QMdiSubWindow()
        sub_window.setWindowTitle("도서 테이블")
        sub_window.setMinimumSize(600, 400)  # 서브 창의 최소 크기 설정
        layout = QVBoxLayout()

        self.book_table = QTableWidget(0, 4)
        self.book_table.setHorizontalHeaderLabels(['일련번호', '제목', '저자', 'ISBN'])
        layout.addWidget(self.book_table)

        # 입력 상자 추가
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("제목")
        layout.addWidget(self.title_input)

        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("저자")
        layout.addWidget(self.author_input)

        self.isbn_input = QLineEdit()
        self.isbn_input.setPlaceholderText("ISBN")
        layout.addWidget(self.isbn_input)

        # 추가 버튼
        add_button = QPushButton("추가")
        add_button.clicked.connect(self.add_book)
        layout.addWidget(add_button)

        sub_window.setLayout(layout)
        self.mdi.addSubWindow(sub_window)
        sub_window.show()

        self.load_books()  # 서브 창이 열릴 때 도서 목록을 불러옵니다.

    def add_book(self):
        title = self.title_input.text()
        author = self.author_input.text()
        isbn = self.isbn_input.text()

        if title and author and isbn:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)", (title, author, isbn))
            self.conn.commit()
            self.load_books()  # 도서 목록 새로 고침
            self.title_input.clear()
            self.author_input.clear()
            self.isbn_input.clear()

    def load_books(self):
        self.book_table.setRowCount(0)  # 기존 데이터 삭제
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM books")
        for row in cursor.fetchall():
            row_position = self.book_table.rowCount()
            self.book_table.insertRow(row_position)
            for column, data in enumerate(row):
                self.book_table.setItem(row_position, column, QTableWidgetItem(str(data)))

    def open_user_table(self):
        sub_window = QMdiSubWindow()
        sub_window.setWindowTitle("사용자 테이블")
        layout = QVBoxLayout()

        self.user_table = QTableWidget(0, 3)
        self.user_table.setHorizontalHeaderLabels(['일련번호', '이름', '연락처'])
        layout.addWidget(self.user_table)

        # 입력 상자 추가
        self.user_name_input = QLineEdit()
        self.user_name_input.setPlaceholderText("이름")
        layout.addWidget(self.user_name_input)

        self.user_contact_input = QLineEdit()
        self.user_contact_input.setPlaceholderText("연락처")
        layout.addWidget(self.user_contact_input)

        # 추가 버튼
        add_user_button = QPushButton("추가")
        add_user_button.clicked.connect(self.add_user)
        layout.addWidget(add_user_button)

        sub_window.setLayout(layout)
        self.mdi.addSubWindow(sub_window)
        sub_window.show()

    def add_user(self):
        name = self.user_name_input.text()
        contact = self.user_contact_input.text()

        if name and contact:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO users (name, contact) VALUES (?, ?)", (name, contact))
            self.conn.commit()
            self.load_users()  # 사용자 목록 새로 고침
            self.user_name_input.clear()
            self.user_contact_input.clear()

    def load_users(self):
        self.user_table.setRowCount(0)  # 기존 데이터 삭제
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            row_position = self.user_table.rowCount()
            self.user_table.insertRow(row_position)
            for column, data in enumerate(row):
                self.user_table.setItem(row_position, column, QTableWidgetItem(str(data)))

    def open_loan_table(self):
        sub_window = QMdiSubWindow()
        sub_window.setWindowTitle("대출현황 테이블")
        layout = QVBoxLayout()

        self.loan_table = QTableWidget(0, 2)
        self.loan_table.setHorizontalHeaderLabels(['일련번호', '대출상태'])
        layout.addWidget(self.loan_table)

        # 입력 상자 추가
        self.loan_status_input = QLineEdit()
        self.loan_status_input.setPlaceholderText("대출 상태")
        layout.addWidget(self.loan_status_input)

        # 추가 버튼
        add_loan_button = QPushButton("추가")
        add_loan_button.clicked.connect(self.add_loan)
        layout.addWidget(add_loan_button)

        sub_window.setLayout(layout)
        self.mdi.addSubWindow(sub_window)
        sub_window.show()

    def add_loan(self):
        status = self.loan_status_input.text()

        if status:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO loans (status) VALUES (?)", (status,))
            self.conn.commit()
            self.load_loans()  # 대출 목록 새로 고침
            self.loan_status_input.clear()

    def load_loans(self):
        self.loan_table.setRowCount(0)  # 기존 데이터 삭제
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM loans")
        for row in cursor.fetchall():
            row_position = self.loan_table.rowCount()
            self.loan_table.insertRow(row_position)
            for column, data in enumerate(row):
                self.loan_table.setItem(row_position, column, QTableWidgetItem(str(data)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_db = MainDB()
    main_db.show()
    sys.exit(app.exec_())
