from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt, pyqtSlot
from PyQt5.QtGui import QFont, QTextLine
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, \
	QWidget
import sys

sys.path.insert(0, './Program')
from database import MyDb
import sqlite3


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.db = my_db(sqlite3.connect('db.sqlite'))
		self.db.debug_print("Authorization")

		print("Interface initialized.")

		self.setWindowTitle("IMag")
		self.setFixedSize(QSize(1000, 600))

		self.login_area = QWidget(self)
		self.setCentralWidget(self.login_area)

		self.login_text = QLabel("Войти", self.login_area)
		self.login_text.setGeometry(440, 224, 120, 16)
		self.login_text.setAlignment(Qt.AlignCenter)

		self.login_linedit = QLineEdit("", self.login_area)
		self.login_linedit.setGeometry(440, 240, 120, 30)

		self.password_text = QLabel("Password", self.login_area)
		self.password_text.setGeometry(440, 274, 120, 16)
		self.password_text.setAlignment(Qt.AlignCenter)

		self.password_lineedit = QLineEdit("", self.login_area)
		self.password_lineedit.setGeometry(440, 290, 120, 30)
		self.password_lineedit.setEchoMode(QLineEdit.Password)

		self.authorize_button = QPushButton("Log in", self.login_area)
		self.authorize_button.setGeometry(460, 330, 80, 40)
		self.authorize_button.clicked.connect(self.login)

		self.show()

	def login(self):
		response = self.db.check_user_in_authorization(self.login_linedit.text(), self.password_lineedit.text())
		self.initialize_main_window()
		if response == 1:
			self.initialize_main_window()
			print("Password is correct. Opening main view.")
		else:
			self.password_lineedit.setText("")
			print("Password is not correct. Login", self.login_linedit.text(),
				  ", Password:" + self.password_lineedit.text())

	def initialize_main_window(self):
		self.login_area.setParent(None)
		print('Initialized.')

		self.main_area = QWidget(self)
		self.setCentralWidget(self.main_area)

		self.main_table = QTableWidget(self.main_area)
		self.main_table.setGeometry(20, 80, 960, 500)
		self.main_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
		self.main_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn);

		self.history_button = QPushButton('История покупок', self.main_area)
		self.history_button.setGeometry(20, 20, 100, 25)
		self.history_button.clicked.connect(self.show_history)

		self.bought_products_button = QPushButton('Найти покупки', self.main_area)
		self.bought_products_button.setGeometry(130, 20, 230, 25)
		self.bought_products_button.clicked.connect(self.show_bought_products)

		self.bought_products_name_lineedit = QLineEdit(self.main_area)
		self.bought_products_name_lineedit.setPlaceholderText('Имя покупателя')
		self.bought_products_name_lineedit.setGeometry(131, 47, 113, 25)
		self.bought_products_name_lineedit.setAlignment(Qt.AlignCenter)

		self.bought_products_surname_lineedit = QLineEdit(self.main_area)
		self.bought_products_surname_lineedit.setPlaceholderText('Фамилия покупателя')
		self.bought_products_surname_lineedit.setGeometry(246, 47, 113, 25)
		self.bought_products_surname_lineedit.setAlignment(Qt.AlignCenter)

		self.product_buyers_button = QPushButton('Найти покупателей', self.main_area)
		self.product_buyers_button.setGeometry(369, 20, 230, 25)
		self.product_buyers_button.clicked.connect(self.show_product_buyers)

		self.product_buyers_article_lineedit = QLineEdit(self.main_area)
		self.product_buyers_article_lineedit.setPlaceholderText('Артикул')
		self.product_buyers_article_lineedit.setGeometry(370, 47, 229, 25)
		self.product_buyers_article_lineedit.setAlignment(Qt.AlignCenter)

	def show_history(self):
		history = self.db.select_all()
		self.show_table_data(history,
							 ['Название товара', 'Цена', 'Артикул', 'Имя покупателя', 'Фамилия покупателя', 'Скидка',
							  'Название магазина', 'Адрес магазина', 'Дата покупки'])

	def show_bought_products(self):
		bought_products = self.db.get_by_name(self.bought_products_name_lineedit.text(),
											  self.bought_products_surname_lineedit.text())
		self.show_table_data(bought_products,
							 ['Название товара', 'Цена', 'Арткул', 'Название магазина', 'Адрес магазина',
							  'Дата покупки'])

	def show_product_buyers(self):
		bought_products = self.db.get_by_article(self.product_buyers_article_lineedit.text())
		self.show_table_data(bought_products,
							 ['Название товара', 'Цена', 'Фамилия покупателя', 'Имя покупателя', 'Скидка',
							  'Название магазина', 'Адрес магазина', 'Дата покупки'])

	def show_table_data(self, data, lables=['']):
		self.clear_main_table()
		if (len(data)) == 0:
			self.main_table.setColumnCount(1)
			self.main_table.insertRow(0)
			self.main_table.setItem(0, 0, QTableWidgetItem('Информация не найдена'))
			self.main_table.resizeColumnsToContents()
			self.main_table.verticalHeader().setVisible(False)
			self.main_table.horizontalHeader().setVisible(False)
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

	def clear_main_table(self):
		self.main_table.clearContents()
		while self.main_table.rowCount() > 0:
			self.main_table.removeRow(0)
		while self.main_table.columnCount() > 0:
			self.main_table.removeColumn(0)


def init():
	app = QApplication(sys.argv)

	window = MainWindow()
	window.login_linedit.setText('admin')
	window.password_lineedit.setText('1111')

	app.exec()