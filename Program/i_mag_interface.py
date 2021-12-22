from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt, pyqtSlot
from PyQt5.QtGui import QFont, QTextLine
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, \
	QWidget
import pandas as pd
import sys
import os.path

sys.path.insert(0, './Program')
from database import MyDb
import sqlite3


class MainWindow(QMainWindow):
	def __init__(self):
		"""
			Инициализаци окна программы.
		"""
		super().__init__()
		if not os.path.exists('db.sqlite'):
			print('Отсуствует нужный файл базы данных')
			raise ConnectionError

		#self.db = MyDb(sqlite3.connect(sys.path[1]+'/db22.sqlite'))
		self.db = MyDb(sqlite3.connect('db.sqlite'))
		self.setWindowTitle("I-Mag")
		self.setFixedSize(QSize(1200, 600))

		self.login_area = QWidget(self)
		self.setCentralWidget(self.login_area)

		self.login_text = QLabel("Войти", self.login_area)
		self.login_text.setGeometry(440, 224, 320, 16)
		self.login_text.setAlignment(Qt.AlignCenter)

		self.login_linedit = QLineEdit("", self.login_area)
		self.login_linedit.setPlaceholderText('Введите логин')
		self.login_linedit.setGeometry(440, 240, 320, 30)

		self.password_text = QLabel("Пароль", self.login_area)
		self.password_text.setGeometry(440, 274, 320, 16)
		self.password_text.setAlignment(Qt.AlignCenter)

		self.password_lineedit = QLineEdit("", self.login_area)
		self.password_lineedit.setPlaceholderText('Введите пароль')
		self.password_lineedit.setGeometry(440, 290, 320, 30)
		self.password_lineedit.setEchoMode(QLineEdit.Password)

		self.authorize_button = QPushButton("Авторизоваться", self.login_area)
		self.authorize_button.setGeometry(460, 330, 280, 40)
		self.authorize_button.clicked.connect(self.login)

		self.show()

	def login(self):
		"""
			Авторизация при помощи запроса к базе данных.
		"""
		response = self.db.check_user_in_authorization(self.login_linedit.text(), self.password_lineedit.text())
		print(self.login_linedit.text(), self.password_lineedit.text(), response)
		self.db.debug_print('Authorization')
		if response == 1:
			self.initialize_main_window()
		else:
			self.password_lineedit.setText('')

	def initialize_main_window(self):
		"""
			Загрузка элементов главной таблицы.
		"""
		self.login_area.setParent(None)
		print('Инициализировано.')

		self.main_area = QWidget(self)
		self.setCentralWidget(self.main_area)

		self.main_table = QTableWidget(self.main_area)
		self.main_table.setSortingEnabled(True)
		self.main_table.setGeometry(20, 80, 1160, 500)
		self.main_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
		self.main_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn);

		self.history_button = QPushButton('Все покупки', self.main_area)
		self.history_button.setGeometry(20, 20, 100, 25)
		self.history_button.clicked.connect(self.show_history)

		self.bought_products_button = QPushButton('Найти покупки', self.main_area)
		self.bought_products_button.setGeometry(130, 20, 230, 25)
		self.bought_products_button.clicked.connect(self.show_bought_products)

		self.bought_products_name_lineedit = QLineEdit(self.main_area)
		self.bought_products_name_lineedit.setPlaceholderText('Имя')
		self.bought_products_name_lineedit.setGeometry(131, 47, 113, 25)
		self.bought_products_name_lineedit.setAlignment(Qt.AlignCenter)

		self.bought_products_surname_lineedit = QLineEdit(self.main_area)
		self.bought_products_surname_lineedit.setPlaceholderText('Фамилия')
		self.bought_products_surname_lineedit.setGeometry(246, 47, 113, 25)
		self.bought_products_surname_lineedit.setAlignment(Qt.AlignCenter)

		self.product_buyers_button = QPushButton('Найти покупателей', self.main_area)
		self.product_buyers_button.setGeometry(369, 20, 230, 25)
		self.product_buyers_button.clicked.connect(self.show_product_buyers)

		self.product_buyers_article_lineedit = QLineEdit(self.main_area)
		self.product_buyers_article_lineedit.setPlaceholderText('Артикул')
		self.product_buyers_article_lineedit.setGeometry(370, 47, 229, 25)
		self.product_buyers_article_lineedit.setAlignment(Qt.AlignCenter)

		self.show_buyers_button = QPushButton('Показать покупателей', self.main_area)
		self.show_buyers_button.setGeometry(609, 20, 230, 25)
		self.show_buyers_button.clicked.connect(self.show_buyers)
		
		self.add_buyers_button = QPushButton('Добавить покупателя', self.main_area)
		self.add_buyers_button.setGeometry(609, 47, 230, 25)
		self.add_buyers_button.clicked.connect(self.show_addbuyer_dialog)

		
		self.save_button = QPushButton('Сохранить в Excel', self.main_area)
		self.save_button.setGeometry(847, 20, 230, 25)
		self.save_button.clicked.connect(self.save_to_excel)
		
		self.filename_lineedit = QLineEdit(self.main_area)
		self.filename_lineedit.setGeometry(847, 47, 230, 25)
		self.filename_lineedit.setPlaceholderText('Название файла')
		self.filename_lineedit.setAlignment(Qt.AlignCenter)


	def save_to_excel(self):
		"""
			Сохранение данных таблицы в эксель файл.
		"""
		if (self.filename_lineedit.text() == ''):
			return

		table = self.main_table
		number_of_rows = table.rowCount()
		number_of_columns = table.columnCount()

		labels_list = []

		for i in range(number_of_columns):
			header = table.horizontalHeaderItem(i)
			if header is not None:
				labels_list.append(header.text())
		if (len(labels_list) == 0):
			self.display_error('Невозможно сохранить пустую таблицу!')
			return

		tmp_df = pd.DataFrame( 
					columns=labels_list, # Fill columnets
					index=range(number_of_rows) # Fill rows
					) 

		for i in range(number_of_rows):
			for j in range(number_of_columns):
				tmp_df.iloc[i, j] = table.item(i, j).data(0)

		tmp_df.to_excel(excel_writer=self.filename_lineedit.text()+'.xlsx', index=False)
		print('Сохранено')

	def show_history(self):
		"""
			Загрузка записей покупок в окно главной таблицы.
		"""
		history = self.db.select_all()
		self.show_table_data(history,
							 ['Название товара', 'Цена', 'Артикул', 'Имя покупателя', 'Фамилия покупателя', 'Скидка', 'Телефон','Клубный статус',
							  'Название магазина', 'Адрес магазина', 'Дата покупки'])

	def show_bought_products(self):
		"""
			Загрузка записей о покупках в окно главной таблицы.
		"""
		bought_products = self.db.get_by_name(self.bought_products_name_lineedit.text(),
											  self.bought_products_surname_lineedit.text())
		self.show_table_data(bought_products,
							 ['Название товара', 'Цена', 'Арткул', 'Название магазина', 'Адрес магазина',
							  'Дата покупки'])

	def show_product_buyers(self):
		"""
			Загрузка записей о покупателях для конкретного товара в окно главной таблицы.
		"""
		bought_products = self.db.get_by_article(self.product_buyers_article_lineedit.text())
		self.show_table_data(bought_products,
							 ['Название товара', 'Цена', 'Фамилия покупателя', 'Имя покупателя', 'Скидка', 'Телефон','Клубный статус',
							  'Название магазина', 'Адрес магазина', 'Дата покупки'])

	def show_buyers(self):
		"""
			Загрузка записей о всех покупателях и их клубных картах в окно главной таблицы.
		"""
		bought_products = self.db.get_buyers()
		self.show_table_data(bought_products,
							 ['Имя покупателя', 'Фамилия покупателя', 'Скидка', 'Телефон','Клубный статус'])

	def show_table_data(self, data, lables=['']):
		"""
			Преобразование ответа базы данных в строки таблицы и их вывод на экран.
		"""
		self.clear_main_table()
		if (len(data)) == 0:
			self.display_error('Информация не найдена')
			print('No data found to fill the table.')
			return
		self.main_table.verticalHeader().setVisible(True)
		self.main_table.horizontalHeader().setVisible(True)
		self.main_table.setColumnCount(len(data[0]))
		for i in range(len(data)):
			self.main_table.insertRow(i)
			entry = data[i]
			for j in range(len(entry)):
				item = QTableWidgetItem(str(entry[j]))
				item.setFlags(QtCore.Qt.ItemIsEnabled)
				self.main_table.setItem(i, j, item)
		self.main_table.setHorizontalHeaderLabels(lables)
		self.main_table.resizeColumnsToContents()

	def display_error(self, text):
		"""
			Вывод сообщения об отсутсвии записей в ответном сообщении.
		"""
		self.main_table.setColumnCount(1)
		self.main_table.insertRow(0)
		self.main_table.setItem(0, 0, QTableWidgetItem(text))
		self.main_table.resizeColumnsToContents()
		self.main_table.verticalHeader().setVisible(False)
		self.main_table.horizontalHeader().setVisible(False)

	def clear_main_table(self):
		"""
			Очистка главной таблицы.
		"""
		self.main_table.clearContents()
		while self.main_table.rowCount() > 0:
			self.main_table.removeRow(0)
		while self.main_table.columnCount() > 0:
			self.main_table.removeColumn(0)

	def show_addbuyer_dialog(self):
		"""
			Вывод диалогового окна добавления покупателя.
		"""
		self.dialog = QDialog()
		self.dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.dialog.setWindowTitle("Добавление покупателя")
		self.dialog.setFixedSize(QSize(400, 300))

		self.dialog.paramEditBoxes = []
		self.dialog.paramNameLabels = []
		paramNames = ['Имя покупателя', 'Фамилия покупателя', 'Скидка', 'Телефон', 'Клубный статус']

		for i in range(0, len(paramNames)):
			self.add_dialog_param(self.dialog, i, paramNames[i])

		self.dialog.add_buyer_button = QPushButton('Добавить', self.dialog)
		self.dialog.add_buyer_button.setGeometry(150, 265, 100, 25)
		self.dialog.add_buyer_button.clicked.connect(self.add_buyer)
		
		self.dialog.show()
		self.dialog.exec()

	def add_buyer(self):
		"""
			Добавление покупателя
		"""
		params = self.dialog.paramEditBoxes
		self.db.insert_into_buyers(params[0].text(), params[1].text(), params[2].text(), params[3].text(), params[4].text())
		self.dialog.close()
		self.show_buyers()

	def add_dialog_param(self, dialog, i, paramName):
		"""
			Загрузка полей в диалоговое окно добавления покупателя.
		"""
		text = QLabel(paramName, dialog)
		text.setGeometry(10, 10+i*40, 145, 20)
		text.setAlignment(Qt.AlignRight)
		lineedit = QLineEdit("", dialog)
		lineedit.setGeometry(175, 10+i*40, 165, 20)
		dialog.paramEditBoxes.append(lineedit)
		dialog.paramNameLabels.append(text)

def init():
	"""
		Запуск окна программы.
	"""
	app = QApplication(sys.argv)

	#343d46
	#4f5b66
	#65737e
	#a7adba
	#c0c5ce

	app.setStyleSheet("""
		QLabel { color: #343d46; font-family: Verdana, sans-serif; font-weight: bold;}
		QLineEdit { border: 1px solid #343d46; background-color: #ffffff; border-radius: 10px; color: #343d46; font-family: Verdana, sans-serif; font-weight: bold;}
		QPushButton { border: 1px solid #343d46;  background-color: #65737e; border-radius: 10px; color: #ffffff; font-family: Verdana, sans-serif; font-weight: bold;}
		QTableView { background-color: #ffffff; color: #000000; font-family: Verdana, sans-serif; }
		QMainWindow { background-color: #c0c5ce}
		QHeaderView::section { border: 1px solid #343d46;  background-color: #65737e; color: #ffffff; font-family: Verdana, sans-serif; font-weight: bold;}
		QScrollBar { margin: -2px -2px -2px -2px; border: 2px solid #343d46;  background-color: #65737e; border-radius: 5px; color: #65737e; }
	""")

	window = MainWindow()
	window.login_linedit.setText('admin')
	window.password_lineedit.setText('1111')

	app.exec()

if __name__ == "__main__":
	init()