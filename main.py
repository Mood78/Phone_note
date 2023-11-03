import tkinter as tk
from tkinter import ttk
import sqlite3
import tkinter.messagebox as mb

# Класс главного окна
class Main(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        self.init_main = ()
        self.db = db        
        self.view_records = ()

###############################################
    # Создание и работа с гланым окном
    def init_main(self):
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
############################################### Кнопки

        # ДОБАВИТЬ
        self.add_img = tk.PhotoImage(file='./img/add.png')
        btn_add = tk.Button(toolbar, bg='#d7d7d7',bd=0,
                            image=self.add_img, command=self.open_child)
        btn_add.pack(side=tk.LEFT)

        # ИЗМЕНИТЬ
        self.upd_img = tk.PhotoImage(file='./img/update.png')
        btn_upd = tk.Button(toolbar, bg='#d7d7d7',bd=0,
                            image=self.upd_img, command=self.open_update_dialog)
        btn_upd.pack(side=tk.LEFT)
        
        # УДАЛИТЬ
        self.del_img = tk.PhotoImage(file='./img/delete.png')
        btn_del = tk.Button(toolbar, bg='#d7d7d7',bd=0,
                            image=self.del_img, command=self.delete_records)
        btn_del.pack(side=tk.LEFT)

        # ПОИСК
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d7d7',bd=0,
                            image=self.search_img, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        # ОБНОВИТЬ
        self.ref_img = tk.PhotoImage(file='./img/refresh.png')
        btn_ref = tk.Button(toolbar, bg='#d7d7d7',bd=0,
                            image=self.ref_img, command=self.view_records)
        btn_ref.pack(side=tk.LEFT)
###############################################

        # Добавляем таблицы
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'phone', 'email', 'salary'),
                                 height=45, show='headings')
        
        # Добавляем параметры колонкам
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary',width=150,anchor=tk.CENTER)

        # Подписи колонок
        self.tree.heading('ID', text="ID")
        self.tree.heading('name', text="ФИО")
        self.tree.heading('phone', text="Телефон")
        self.tree.heading('email', text="E-mail")
        self.tree.heading('salary', text="Зарплата")

        # Упаковка
        self.tree.pack(side=tk.LEFT)

        # Ползунок
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)

        self.tree.configure(yscrollcommand=scroll.set)

############################################### ОСНОВНЫЕ МЕТОДЫ

    def records(self, name, phone, email,salary):
        self.db.insert_data(name, phone, email,salary)
        self.view_records()
    # Отображение данных TreeView
    def view_records(self):
        self.db.cur.execute("""SELECT * FROM users""")

        [self.tree.delete (i) for i in self.tree.get_children()]
        [self.tree.insert('','end', values=row)
         for row in self.db.cur.fetchall()]
        
    # Метод обновления данных
    def update_record(self, name, phone, email,salary):
        sta = name.replace(" ",'')
        st = sta.isalpha()
        intt = phone.isdigit()
        itn = salary.isdigit()
        id = self.tree.set(self.tree.selection()[0], '#1')

        if st == True and intt == True and itn == True:
            self.db.cur.execute(""" UPDATE users SET name=?, phone=?, email=?, salary=? WHERE ID=?""",
                                (name, phone, email, salary, id))
            self.db.conn.commit()
            self.view_records()
        else:
            msg = 'Введённые данные некорректны'
            mb.showerror("Ошибка",msg)
            


    # Метод удаления данных
    def delete_records(self):
        for row in self.tree.selection():
            self.db.cur.execute("""DELETE FROM users WHERE ID=?""",
                                (self.tree.set(row, '#1'),))
        self.db.conn.commit()
        self.view_records()

    # Метод поиска данных
    def search_records(self, name):
        name = ('%'+ name +'%')
        self.db.cur.execute("""SELECT * FROM users WHERE name LIKE ?""", (name, ))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end', values=row)
         for row in self.db.cur.fetchall()]

############################################### ВЫЗОВЫ КЛАССОВ
    
    # метод вызывающий окно добавления
    def open_child(self):
        Child()

    # метод вызывающий окно обновления
    def open_update_dialog(self):
        Update()

    # метод вызывающий окно поиска
    def open_search_dialog(self):
        Search()

###############################################
###############################################

# Создание окна Добавления
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # Создание и работа с дочерними окнами
    def init_child(self):
        self.title('Добавить контакт')
        self.geometry('400x200')
        self.resizable(False,False)
        # Перехватываем все события происходящие в приложении
        self.grab_set()
        # Захватываем фокус
        self.focus_set()
        
###############################################
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text='Телефон')
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail')
        label_email.place(x=50, y=110)
        label_salary = tk.Label(self, text='Зарплата')
        label_salary.place(x=50, y=140)
        
        self.entry_name = ttk.Entry(self)
        self.entry_name.place (x=200, y =50)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)
###############################################
        # Кнопка закрытия
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)
        
        # Кнопка добавления
        self.btn_add = ttk.Button(self, text='Добавить')
        self.btn_add.place(x=220, y=170)
        self.btn_add.bind('<Button-1>', lambda event:
                          self.view.records(self.entry_name.get(),
                                            self.entry_phone.get(),
                                            self.entry_email.get(),
                                            self.entry_salary.get()))
###############################################
###############################################

# Класс редакирования
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db = db
        self.default_data()

    def init_update(self):
        self.title('Редактировать позицию')
        self.btn_add.destroy()

        self.btn_upd = ttk.Button(self, text='Редактировать')
        self.btn_upd.bind('<Button-1>', lambda event:
                          self.view.update_record(self.entry_name.get(),
                                                  self.entry_phone.get(),
                                                  self.entry_email.get(),
                                                  self.entry_salary.get()))
        self.btn_upd.bind('<Button-1>', lambda event: self.destroy(), add='+')
    
        self.btn_upd.place(x=200, y=170)

    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute("""SELECT * FROM users WHERE ID=?""",(id, ))

        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])
        


###############################################
###############################################

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Поиск по контактам')
        self.geometry('300x100')
        self.resizable(False,False)
        self.grab_set()
        self.focus_set()

###############################################      
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=20, y=20)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=70, y=20)

###############################################
        # Кнопка закрытия
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=200, y=170)
        
        # Кнопка поиска
        self.btn_search = ttk.Button(self, text='Найти')
        self.btn_search.place(x=70, y=70)
        self.btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_name.get()))

###############################################
###############################################
# Класс Базы данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('Employee.db')
        self.cur = self.conn.cursor()
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            phone INTEGER,
                            email TEXT,
                            salary INTEGER) """)
        self.conn.commit()

    def insert_data (self, name, phone, email, salary):
        st =name.replace(' ','')
        sta= st.isalpha()
        intt = phone.isdigit()
        itn = salary.isdigit()
        # Проверка на правильность введённых данных
        if   sta == True and intt == True and itn == True:
            self.cur.execute(""" INSERT INTO users(name, phone, email, salary)
            VALUES (?,?,?,?)""", (name, phone, email, salary))
            self.conn.commit()
        else:
            msg = 'Введённые данные некорректны'
            mb.showerror("Ошибка",msg)
        
          
###############################################
# Создание окна
if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main (root)
    app.pack()
    root.title('Список сотрудников компании')
    root.geometry('795x600')
    root.resizable(False,False)
    root.configure(bg='White')
    root.mainloop()
