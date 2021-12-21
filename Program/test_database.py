"""
For full test lauch - make in cmd "python -m unittest"
"""
import unittest
from database import MyDb
import sqlite3


class TestMyDb(unittest.TestCase):
    def setUp(self):
        self.mydb = MyDb(sqlite3.connect('db.sqlite'))

    def test_select_all(self):
        """
        Проверка на то, что метод возвращает ожидаемый тип - list
        :return:
        """
        self.assertEqual(type(self.mydb.select_all()), list, 'Полученное значение не является списком!')
        # self.assertEqual(type(self.mydb.select_all()), tuple, 'Полученное значение не является кортежем!')

    def test_get_buyers(self):
        """
        Проверка на то, что метод возвращает ожидаемый тип - list
        :return:
        """
        self.assertEqual(type(self.mydb.get_buyers()), list, 'Полученное значение не является списком!')

    def test_get_by_name(self):
        """
        Проверка на то,что методу подаются строки и он возвращает список
        :return:
        """
        self.assertRaises(TypeError, self.mydb.get_by_name(1, 3))  # Проведя этот тест было выяснено, что в методе
        # get_by_name нет проверки на тип
        self.assertEqual(type(self.mydb.get_by_name('Дима', 'Усенко')), list,
                         'Полученное значение не является списком!')

    def test_get_by_article(self):
        """
        Проверка на то,что методу передается int и он возвращает список
        :return:
        """
        self.assertRaises(TypeError, self.mydb.get_by_article(10012438300))  # Проведя этот тест было выяснено, что в
        # методе get_by_article нет проверки на тип
        self.assertEqual(type(self.mydb.get_by_article("10012438300")), list,
                         'Полученное значение не является списком!')

    def test_check_user_in_authorization(self):
        """
        Проверка на то, что методу передаются строки и на то, что возвращается правильное значение
        :return:
        """
        self.assertRaises(TypeError, self.mydb.check_user_in_authorization('admin', 1111))
        self.assertEqual(self.mydb.check_user_in_authorization("admin", "1111"), 1, 'Возвращается неверное значение')

    def test_insert_into_buyers(self):
        """
        Проверка на то, что методу передаются аргументы с правильынм типом данных
        :return:
        """
        self.assertRaises(TypeError, self.mydb.insert_into_buyers('Вася', 'Никитин', '0.1', '52-01-01', 'Золото'))
        # self.assertRaises(TypeError, self.mydb.insert_into_buyers(1, 'Никитин', 0.1, '52-01-01', 'Золото'))
