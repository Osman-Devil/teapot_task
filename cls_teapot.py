import time
import keyboard
import logging
import configparser
import sqlite3

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("setting.ini")  # читаем конфиг

# получение пользовательского логгера и установка уровня логирования
py_logger = logging.getLogger(__name__)
py_logger.setLevel(logging.INFO)

# настройка обработчика и форматировщика в соответствии с нашими нуждами
py_handler = logging.FileHandler(f"{__name__}.log", mode='w', encoding="utf-8")
py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

# добавление форматировщика к обработчику
py_handler.setFormatter(py_formatter)
# добавление обработчика к логгеру
py_logger.addHandler(py_handler)


class Teapot:  # Основной класс Teapot
    def __init__(self, boil_time=1, temperature=0):
        self.boil_time = boil_time
        self.temperature = temperature

    # Функция, чтобы задать количество воды
    def amount_of_water_teapot(self):
        # Обращаемся в setting.ini к значению amount_of_water
        value_water = config["Teapot"]["amount_of_water"]
        amount_of_water = "Задайте количество воды объемом до 1.0л :  " + value_water
        py_logger.info(amount_of_water)
        if value_water == 0:
            py_logger.info("Чайник не может быть включен, так как нету воды")
        elif 0 < float(value_water) <= 1:
            py_logger.info("Можете включить чайник")
            self.on_off_teapot()
        else:
            py_logger.info("Заполните чайник до 1 литра")
        return self

    # Функция вкл/выкл
    def on_off_teapot(self):
        # Обращаемся в setting.ini к значению status
        value_status = config["Teapot"]["status"]
        status = "Задайте 'On' или 'Off' чайнику: " + value_status
        py_logger.info(status)
        if value_status == "On":
            py_logger.info("Чайник включен")
            self.status_of_teapot()
        elif value_status == "Off":
            py_logger.info("Чайник выключен")
        else:
            py_logger.info("Попробуйте еще раз")
        return self

    # Функция закипания и выключения чайника
    def status_of_teapot(self):
        py_logger.info("Зажмите 'p', чтобы выключить. Выключится сама через 10 секунд")
        print("Зажмите 'p', чтобы выключить. Выключится сама через 10 секунд")
        while True:  # Цикл, которая показывает температуру от времени
            py_logger.info(self.boil_time)
            time.sleep(1)
            self.boil_time += 1
            self.temperature += 10
            py_logger.info(f"Температура: {self.temperature}°C")
            if keyboard.is_pressed("p"):  # Условие выключения по нажатию клавиши
                py_logger.info("Остановлен")
                break
            elif self.boil_time > 10:  # Условие выключения при закипании
                py_logger.info("Вскипел")
                break

    # Функция записи в базу SQLite3
    def write_to_db(self):
        try:
            sqlite_connection = sqlite3.connect('sqlite_python.db')
            cursor = sqlite_connection.cursor()  # Создание курсора
            print("Подключен к SQLite")

            # Создание таблицы teopot в бд
            cursor.execute("""CREATE TABLE IF NOT EXISTS teapot(
                            id INTEGER PRIMARY KEY,
                            message TEXT,
                            joiningDate timestamp)""")

            # Открытие файла для записи даты и сообщения в бд
            with open('__main__.log', encoding="UTF-8") as fml:
                for line in fml:
                    result_data = line.strip()[9:28]
                    result_message = line.strip()[38:]
                    cursor.execute(f"INSERT INTO 'teapot'"
                                   f"('message', 'joiningDate')"
                                   f"VALUES (?, ?);", (result_data, result_message))

                fml.close()  # Закрытие файла
            cursor.close()  # Закрытие курсора

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")

        fml.close()
        return self


m = Teapot()
m.amount_of_water_teapot()
m.write_to_db()
