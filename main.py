from src.config import config
from src.db_manager import DBManager
from src.db_setup import create_database, create_tables, save_data_to_db
from src.hh_api import HHApi


def main() -> None:
    """Главная функция программы."""
    employer_ids_list = [
        "872241",
        "10413982",
        "11169700",
        "11337555",
        "5724503",
        "10808234",
        "5845348",
        "1083528",
        "11156224",
        "46926",
    ]
    params = config()

    # Создаем базу данных, таблицы и загружаем туда все данные
    create_database("vacancies_by_employer", params)
    create_tables("vacancies_by_employer", params)

    # Инициализация и загрузка данных из API
    api = HHApi()
    employers_data = api.get_employers(employer_ids_list)

    # Преобразуем vacancies_data в список словарей с вакансиями
    vacancies_data = []
    for employer_id in employer_ids_list:
        vacancies = api.get_vacancies_by_employer(employer_id)
        vacancies_data.extend(vacancies)

    save_data_to_db("vacancies_by_employer", params, vacancies_data, employers_data)

    # Тестирование функций класса DBManager
    db_manager = DBManager("vacancies_by_employer", **params)

    print("Приветствую в программе по поиску вакансий с конкретных работодателей!")
    print("Выберите функцию для тестирования:")

    while True:
        print("\n1: Получить список всех компаний и количество вакансий у каждой компании")
        print(
            "2: Посмотреть список всех вакансий с указанием имени компании, вакансии, ЗП и ссылки на вакансию"
        )
        print("3: Получить среднюю зарплату по вакансиям")
        print("4: Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям")
        print("5: Список всех вакансий, в названии которых содержатся переданные в метод слова, например python")
        print("6: Выйти")

        number = input("\nВведите номер действия: ")

        if number == "1":
            print(db_manager.get_companies_and_vacancies_count())
        elif number == "2":
            print(db_manager.get_all_vacancies())
        elif number == "3":
            print(db_manager.get_avg_salary())
        elif number == "4":
            print(db_manager.get_vacancies_with_higher_salary())
        elif number == "5":
            keyword = input("Введите ключевое слово: ")
            print(db_manager.get_vacancies_with_keyword(keyword))
        elif number == "6":
            print("Выход из программы.")
            break
        else:
            print("Неверное действие. Попробуйте снова.")


if __name__ == "__main__":
    main()
