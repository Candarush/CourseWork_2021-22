import sqlite3

class my_db():

    def __init__(self, bd):
        self.bd = bd
        self.curr = bd.cursor()
        self.curr.execute("""
                create table if not exists Authorization(
                    authorization_id integer primary key autoincrement,
                    login char(16),
                    password char(16)
                )""")
        self.curr.execute("""
                create table if not exists Products(
                    product_id integer primary key autoincrement,
                    name char(16),
                    price integer,
                    article char(20)
                )""")
        self.curr.execute("""
                create table if not exists Buyers(
                    buyer_id integer primary key autoincrement,
                    name char(16),
                    surname char(16),
                    discount double 
                )""")
        self.curr.execute("""
                create table if not exists Store(
                    store_id integer primary key autoincrement,
                    name char(16),
                    address char(64) 
                )""")
        self.curr.execute("""
                create table if not exists History(
                    history_id integer primary key autoincrement,
                    product_id integer,
                    buyer_id integer,
                    store_id integer,
                    buy_date date,
                    foreign key (product_id) references products (product_id),
                    foreign key (buyer_id) references buyers (buyer_id),
                    foreign key (store_id) references store (store_id)
                    )""")
        self.bd.commit()

    def select_all(self):
        """
        Возвращает список кортежей, в каждом кортеже указаны все данные.
        """
        self.curr.execute(""" 
        SELECT Products.name,Products.price,article,Buyers.name,Buyers.surname,
        Buyers.discount,Store.name,Store.address,buy_date FROM History
        join Products on History.product_id=Products.product_id
        join Buyers on History.buyer_id=Buyers.buyer_id
        join Store on History.store_id=Store.store_id
        
        """)
        return self.curr.fetchall()

    def get_by_name(self, name, surname):
        """
        Принимает две строки - имя и фамилия, по которым осуществляется фильтрация.

        Возвращает список из кортежей, где каждый кортеж -  Имя товара, цена, арткул, имя магазина, адрес магазина,
        дата покупки.
        """
        self.curr.execute(f"""
        SELECT Products.name,Products.price,article,Store.name,Store.address,buy_date FROM History
        join Products on History.product_id=Products.product_id
        join Buyers on History.buyer_id=Buyers.buyer_id
        join Store on History.store_id=Store.store_id
        where Buyers.name='{name}' and Buyers.surname='{surname}'""")
        return self.curr.fetchall()

    def get_by_article(self, article):
        """
        Принимает строку - артикул, по которому осуществляется фильтрация

        Возвращает список из кортежей, где каждый кортеж - имя товара,цену товара,имя покупателя, фамилиюю покупателя,
        его скидка, имя магазина, адрес магазина,
        дату покупки.
        """
        self.curr.execute(f"""SELECT Products.name,Products.price,Buyers.name,Buyers.surname,Buyers.discount,Store.name,
        Store.address,buy_date FROM History
        join Products on History.product_id=Products.product_id
        join Buyers on History.buyer_id=Buyers.buyer_id
        join Store on History.store_id=Store.store_id
        where Products.article='{article}'""")
        return self.curr.fetchall()

    def check_user_in_authorization(self, login, password):
        """
        Принимает строки - логин и пароль
        Возвращает 1, если пользователь есть в таблице авторизации
        Возвращает 0, если пользователя нет в таблице авторизации
        """
        self.curr.execute(f"""select count(login) from Authorization
                                where login = '{login}' and password='{password}'""")
        user = self.curr.fetchall()[0][0]
        if user == 1:
            return 1
        elif user == 0:
            return 0

    def close_con(self):
        """Закрывает соединение с базой"""
        self.bd.close()

    def debug_print(self, tablename):
        self.curr.execute(f"""SELECT * FROM '{tablename}'""")
        print(f"{tablename} contents:\n", self.curr.fetchall())



if __name__ == '__main__':
    db = my_db(sqlite3.connect('db.sqlite'))
