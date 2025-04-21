import sqlite3

def create_user_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            join_date TEXT NOT NULL,
            leave_date TEXT,
            loan_count INTEGER DEFAULT 0,
            contact TEXT NOT NULL
        );
    ''')
    conn.commit()

def create_book_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT NOT NULL,
            loan_status TEXT DEFAULT NULL
        );
    ''')
    conn.commit()

def create_rent_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rents (
            id INTEGER PRIMARY KEY,
            book_title TEXT NOT NULL,
            borrower TEXT NOT NULL,
            rent_date TEXT NOT NULL,
            return_date TEXT,
            reservation_status INTEGER DEFAULT 0
        );
    ''')
    conn.commit()

def insert_user(conn, name, join_date, contact):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (name, join_date, contact) VALUES (?, ?, ?);
    ''', (name, join_date, contact))
    conn.commit()

def insert_book(conn, title, author, isbn):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO books (title, author, isbn) VALUES (?, ?, ?);
    ''', (title, author, isbn))
    conn.commit()

def insert_rent(conn, book_title, borrower, rent_date):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO rents (book_title, borrower, rent_date) VALUES (?, ?, ?);
    ''', (book_title, borrower, rent_date))
    conn.commit()
    
    # 대출현황 업데이트
    cursor.execute('''
        UPDATE books SET loan_status = ? WHERE title = ?;
    ''', (borrower, book_title))
    conn.commit()

def view_all_users(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print()

def view_all_books(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print()

def view_all_rents(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rents;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print()

def search_user(conn, search_term):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name LIKE ?;", (f'%{search_term}%',))
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print()

def search_book(conn, search_term):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?;", (f'%{search_term}%', f'%{search_term}%'))
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print()

def search_rent(conn, search_term):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rents WHERE book_title LIKE ? OR borrower LIKE ?;", (f'%{search_term}%', f'%{search_term}%'))
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print()

def update_user(conn, user_id, name, join_date, contact):
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET name = ?, join_date = ?, contact = ? WHERE id = ?;
    ''', (name, join_date, contact, user_id))
    conn.commit()

def update_book(conn, book_id, title, author, isbn):
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE books SET title = ?, author = ?, isbn = ? WHERE id = ?;
    ''', (title, author, isbn, book_id))
    conn.commit()

def update_rent(conn, rent_id, book_title, borrower, rent_date):
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE rents SET book_title = ?, borrower = ?, rent_date = ? WHERE id = ?;
    ''', (book_title, borrower, rent_date, rent_id))
    conn.commit()

def delete_user(conn, user_id):
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM users WHERE id = ?;
    ''', (user_id,))
    conn.commit()

def delete_book(conn, book_id):
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM books WHERE id = ?;
    ''', (book_id,))
    conn.commit()

def delete_rent(conn, rent_id):
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM rents WHERE id = ?;
    ''', (rent_id,))
    conn.commit()

def main_menu():
    print("1. 사용자 정보")
    print("2. 도서 정보")
    print("3. 대출 현황")
    print("4. 종료")
    return input("원하는 작업의 번호를 입력하세요: ")

def view_data_menu():
    print("1. 데이터 보기")
    print("2. 검색")
    print("3. 입력")
    print("4. 수정")
    print("5. 삭제")
    print("6. 종료")
    return input("원하는 작업의 번호를 입력하세요: ")

if __name__ == "__main__":
    user_db_name = "User.db"
    book_db_name = "Book.db"
    rent_db_name = "Rent.db"

    # 테이블 생성
    user_conn = sqlite3.connect(user_db_name)
    create_user_table(user_conn)
    user_conn.close()

    book_conn = sqlite3.connect(book_db_name)
    create_book_table(book_conn)
    book_conn.close()

    rent_conn = sqlite3.connect(rent_db_name)
    create_rent_table(rent_conn)
    rent_conn.close()

    while True:
        choice = main_menu()

        if choice == '1':
            user_conn = sqlite3.connect(user_db_name)
            while True:
                print("1. (사용자) 데이터 보기")
                print("2. 검색")
                print("3. 입력")
                print("4. 수정")
                print("5. 삭제")
                print("6. 종료")
                user_choice = input("원하는 작업의 번호를 입력하세요: ")

                if user_choice == '1':
                    view_all_users(user_conn)  # 사용자 데이터 보기
                elif user_choice == '2':
                    search_term = input("검색할 이름을 입력하세요: ")
                    search_user(user_conn, search_term)
                elif user_choice == '3':
                    name = input("이름 입력: ")
                    join_date = input("가입일 입력: ")
                    contact = input("연락처 입력: ")
                    insert_user(user_conn, name, join_date, contact)
                elif user_choice == '4':
                    user_id = int(input("수정할 사용자의 번호를 입력하세요: "))
                    name = input("새 이름 입력: ")
                    join_date = input("새 가입일 입력: ")
                    contact = input("새 연락처 입력: ")
                    update_user(user_conn, user_id, name, join_date, contact)
                elif user_choice == '5':
                    user_id = int(input("삭제할 사용자의 번호를 입력하세요: "))
                    delete_user(user_conn, user_id)
                elif user_choice == '6':
                    user_conn.close()
                    break
                else:
                    print("잘못된 입력입니다. 다시 시도하세요.")

        elif choice == '2':
            book_conn = sqlite3.connect(book_db_name)
            while True:
                print("1. (도서) 데이터 보기")
                print("2. 검색")
                print("3. 입력")
                print("4. 수정")
                print("5. 삭제")
                print("6. 종료")
                book_choice = input("원하는 작업의 번호를 입력하세요: ")

                if book_choice == '1':
                    view_all_books(book_conn)  # 도서 데이터 보기
                elif book_choice == '2':
                    search_term = input("검색할 도서명 또는 저자를 입력하세요: ")
                    search_book(book_conn, search_term)
                elif book_choice == '3':
                    title = input("도서명 입력: ")
                    author = input("저자 입력: ")
                    isbn = input("ISBN 입력: ")
                    insert_book(book_conn, title, author, isbn)
                elif book_choice == '4':
                    book_id = int(input("수정할 도서의 번호를 입력하세요: "))
                    title = input("새 도서명 입력: ")
                    author = input("새 저자 입력: ")
                    isbn = input("새 ISBN 입력: ")
                    update_book(book_conn, book_id, title, author, isbn)
                elif book_choice == '5':
                    book_id = int(input("삭제할 도서의 번호를 입력하세요: "))
                    delete_book(book_conn, book_id)
                elif book_choice == '6':
                    book_conn.close()
                    break
                else:
                    print("잘못된 입력입니다. 다시 시도하세요.")

        elif choice == '3':
            rent_conn = sqlite3.connect(rent_db_name)
            while True:
                print("1. (대출) 데이터 보기")
                print("2. 검색")
                print("3. 입력")
                print("4. 수정")
                print("5. 삭제")
                print("6. 종료")
                rent_choice = input("원하는 작업의 번호를 입력하세요: ")

                if rent_choice == '1':
                    view_all_rents(rent_conn)  # 대출 데이터 보기
                elif rent_choice == '2':
                    search_term = input("검색할 도서명 또는 대출자를 입력하세요: ")
                    search_rent(rent_conn, search_term)
                elif rent_choice == '3':
                    book_title = input("도서명 입력: ")
                    borrower = input("대출자 입력: ")
                    rent_date = input("대출일자 입력: ")
                    insert_rent(rent_conn, book_title, borrower, rent_date)
                elif rent_choice == '4':
                    rent_id = int(input("수정할 대출 현황의 번호를 입력하세요: "))
                    book_title = input("새 도서명 입력: ")
                    borrower = input("새 대출자 입력: ")
                    rent_date = input("새 대출일자 입력: ")
                    update_rent(rent_conn, rent_id, book_title, borrower, rent_date)
                elif rent_choice == '5':
                    rent_id = int(input("삭제할 대출 현황의 번호를 입력하세요: "))
                    delete_rent(rent_conn, rent_id)
                elif rent_choice == '6':
                    rent_conn.close()
                    break
                else:
                    print("잘못된 입력입니다. 다시 시도하세요.")

        elif choice == '4':
            break
        else:
            print("잘못된 입력입니다. 다시 시도하세요.")

    print("프로그램을 종료합니다.")
