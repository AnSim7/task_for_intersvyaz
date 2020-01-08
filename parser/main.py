"""Модуль разделения данным из файла logs.txt
    Параметры запуска: текстовый файл с расширением .txt
    Версия интерпретатора: Python 3.7.2 64bit
    Для определения страны по ip адресу был использован модуль pysyge. Ссылка для скачивания https://github.com/surpr1ze/python-sxgeo/
    © 2020. Симонова А. 89080567599 simonova_anastasia97@mail.ru"""

from pysyge_master.pysyge.pysyge import GeoLocator, MODE_BATCH, MODE_MEMORY
import csv

class Parser:
    """Класс парсер.
    Конструктор принимает название файла."""
    def __init__(self, filename):
        self.file=filename
        self.arr_of_text_from_logs=[]
        self.arr_of_users=[]
        self.arr_of_ips = []
        self.id_user=1
        self.arr_of_categories=[]
        self.arr_of_categories_table = []
        self.id_category = 1
        self.arr_of_products=[]
        self.arr_of_products_table=[]
        self.id_product = 1
        self.arr_of_transactions= []
        self.id_transaction = 1
        self.arr_of_history = []
        self.id_history = 1

    def parsing(self):
        """Метод для раздления файла на списки:
            список ip адресов arr_of_ips
            список категорий продуктов arr_of_categories
            список продуктов arr_of_products
        А также на многомерные списки, которые соответствуют структурам таблиц базы данных:
            пользователи (id, ip, country) arr_of_users
            категории (id, name) arr_of_categories_table
            продукты (id, name, id_category) arr_of_products_table
            транзакции(покупки) (id, id_user, datetime) arr_of_transactions
            история (id, id_user, datetime, id_category) arr_of_history"""

        geodata = GeoLocator('pysyge_master\pysyge\SxGeoCity.dat', MODE_BATCH | MODE_MEMORY)

        file = open(self.file)
        for line in file:
            print(line)
            string = line.lower().split()
            change_string = []
            change_string.append(string[2] + " " + string[3])
            change_string.append(string[6])

            if string[6] not in self.arr_of_ips:
                arr=[]
                arr.append(self.id_user)
                arr.append(string[6])
                location = geodata.get_location(string[6], detailed=True) # определение страны пользователя
                if len(location)!=0:
                    arr.append(location['info']['country']['name_ru'])
                else:
                    arr.append('')
                self.arr_of_users.append(arr) #заполнение массива пользователей
                self.arr_of_ips.append(string[6])
                self.id_user+=1

            product = []
            product = list(string[7].replace("https://all_to_the_bottom.com/", '').split("/", maxsplit=1))

            if product[0]!='' and 'cart_id' not in product[0] and 'success_pay' not in product[0] and product[0] not in self.arr_of_categories:
                arr=[]
                arr.append(self.id_category)
                arr.append(product[0])
                self.arr_of_categories_table.append(arr)
                self.arr_of_categories.append(product[0])
                self.id_category+=1

            if len(product) == 2 and product[1]!='' and 'cart_id' not in product[0] and 'success_pay' not in product[0] and product[1] not in self.arr_of_products:
                product[1] = product[1].replace("/", '')
                change_string.append(product[0])
                change_string.append(product[1])
                if product[1] not in self.arr_of_products:
                    arr = []
                    i = self.arr_of_categories.index(product[0])
                    arr.append(self.id_product)
                    arr.append(self.arr_of_categories_table[i][0])
                    arr.append(product[1])
                    self.arr_of_products_table.append(arr)
                    self.arr_of_products.append(product[1])
                    self.id_product += 1
            else:
                change_string.append(product[0])

            if 'success_pay' in product[0]:
                arr=[]
                arr.append(self.id_transaction)
                i = self.arr_of_ips.index(string[6])
                arr.append(self.arr_of_users[i][0])
                arr.append(string[2] + " " + string[3])
                self.arr_of_transactions.append(arr)
                self.id_transaction+=1

            arr=[]
            arr.append(self.id_history)
            i = self.arr_of_ips.index(string[6])
            arr.append(self.arr_of_users[i][0])
            arr.append(string[2] + " " + string[3])
            if len(product)>0 and product[0]!='' and 'cart_id' not in product[0] and 'success_pay' not in product[0]:
                i=self.arr_of_categories.index(product[0])
                arr.append(self.arr_of_categories_table[i][0])
            else:
                arr.append('')
            self.arr_of_history.append(arr)
            self.id_history+=1

            self.arr_of_text_from_logs.append(change_string)

        for value in self.arr_of_text_from_logs:
            print(value)
        print(1)

    def get_arr_of_users(self):
        """Метод для получения списка пользователей"""
        return self.arr_of_users

    def get_arr_of_transactions(self):
        """Метод для получения списка транзакция"""
        return self.arr_of_transactions

    def get_arr_of_categories(self):
        """Метод для получения списка категорий"""
        return self.arr_of_categories_table

    def get_arr_of_products(self):
        """Метод для получения списка продуктов"""
        return self.arr_of_products

    def get_arr_of_history(self):
        """Метод для получения списка истории"""
        return self.arr_of_history

    def print_csv_rr_of_users(self, filename, arr):
        """Метод записи данных в файл с расширением .csv
        входные данные: название файла и список, который будет записан в файл"""
        with open(filename, "w") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(arr)


obj=Parser("logs.txt")
obj.parsing()
obj.print_csv_rr_of_users('history.csv', obj.arr_of_history)
