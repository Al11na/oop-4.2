import unittest
import sqlite3
from io import StringIO
from contextlib import redirect_stdout

# Импорт функций из основного файла
from flight_management import create_tables, add_destination, add_flight, display_flights_by_destination

class TestFlightManagementSystem(unittest.TestCase):

    def setUp(self):
        # Создание временной базы данных в памяти
        self.conn = sqlite3.connect(':memory:')
        create_tables(self.conn)

    def tearDown(self):
        # Закрытие соединения после каждого теста
        self.conn.close()

    def test_add_destination(self):
        # Тест добавления пункта назначения
        add_destination(self.conn, 'Москва')
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM Destinations WHERE name = 'Москва'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 'Москва')

    def test_add_flight(self):
        # Тест добавления рейса
        add_destination(self.conn, 'Париж')
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM Destinations WHERE name = 'Париж'")
        destination_id = cursor.fetchone()[0]

        add_flight(self.conn, destination_id, 'SU123', 'Boeing 737')
        cursor.execute("SELECT flight_number FROM Flights WHERE flight_number = 'SU123'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 'SU123')

    def test_display_flights_by_destination(self):
        # Тест отображения рейсов по пункту назначения
        add_destination(self.conn, 'Лондон')
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM Destinations WHERE name = 'Лондон'")
        destination_id = cursor.fetchone()[0]

        add_flight(self.conn, destination_id, 'BA456', 'Airbus A320')

        # Перехват вывода на консоль
        with StringIO() as buf, redirect_stdout(buf):
            display_flights_by_destination(self.conn, 'Лондон')
            output = buf.getvalue()

        # Проверяем, что вывод содержит нужную информацию
        self.assertIn('BA456', output)
        self.assertIn('Airbus A320', output)

if __name__ == '__main__':
    unittest.main()
