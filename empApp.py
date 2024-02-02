import tkinter as tk
from tkinter import messagebox
import sqlite3
import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r"C:\Program Files\Oracle\instantclient_19_9")

class EmpManApp:
    # 클래스 레벨에서 데이터베이스 연결 설정
    username = "system"
    password = "121212"
    dsn = "localhost:1521/xe"
    connection = cx_Oracle.connect(username, password, dsn)

    def __init__(self, master):
        self.master = master
        self.master.title("Employee Management System")
        self.master.geometry("800x600")
        
        self.search_label = tk.Label(master, text="Enter Employee Name:")
        self.search_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        
        self.search_entry = tk.Entry(master)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        
        self.search_button = tk.Button(master, text="Search by Name", command=self.search_by_name)
        self.search_button.grid(row=0, column=2, padx=10, pady=10, sticky=tk.W)
        
        self.result_text = tk.Text(master, height=20, width=100)
        self.result_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
    
    def display_result(self, results, columns):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"{' | '.join(columns)}\n")
        self.result_text.insert(tk.END, "-" * (len(columns) * 20) + "\n")
        for row in results:
            self.result_text.insert(tk.END, f"{row}\n")
    
    def search_by_name(self):
        name = self.search_entry.get()
        
        try:
            cursor = self.connection.cursor()
            
            # SQL 쿼리 실행
            sql_query = f"SELECT * FROM emp WHERE ename LIKE '%{name}%'"
            cursor.execute(sql_query)
            
            # 결과 가져오기
            rows = cursor.fetchall()
            
            # 컬럼명 가져오기
            columns = [col[0] for col in cursor.description]
            
            # 결과 출력
            self.display_result(rows, columns)
            
            # 커서 닫기
            cursor.close()
        except cx_Oracle.Error as error:
            self.display_result([("Error while connecting to Oracle Database", error)], [])

def main():
    root = tk.Tk()
    app = EmpManApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
