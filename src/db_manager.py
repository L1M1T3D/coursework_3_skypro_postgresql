from typing import Any, List

import psycopg2


class DBManager:
    """Класс для работы с компаниями и вакансиями в БД PostgreSQL с использованием psycopg2."""

    def __init__(self, database_name: str, **params: str) -> None:
        self.conn = psycopg2.connect(dbname=database_name, **params)
        self.cursor = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> list[tuple[Any, ...]]:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        self.cursor.execute(
            """
            SELECT employer_name, open_vacancies FROM employers
        """
        )
        return self.cursor.fetchall()

    def get_all_vacancies(self) -> list[tuple[Any, ...]]:
        """Получает список всех вакансий с указанием имени компании, вакансии, ЗП и ссылки на вакансию."""
        self.cursor.execute(
            """
            SELECT employers.employer_name, vacancies.vacancy_name, vacancies.salary_from,
            vacancies.salary_to, vacancies.url
            FROM vacancies
            JOIN employers ON vacancies.employer_id = employers.id
        """
        )
        return self.cursor.fetchall()

    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по вакансиям."""
        self.cursor.execute(
            """
            SELECT AVG((salary_from + salary_to) / 2) AS avg_salary FROM vacancies
            WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
        """
        )
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> list[tuple[Any, ...]]:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        avg_salary = self.get_avg_salary()
        self.cursor.execute(
            """
            SELECT vacancy_name, salary_from, salary_to FROM vacancies
            WHERE (salary_from + salary_to) / 2 > %s
        """,
            (avg_salary,),
        )
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[str]:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        self.cursor.execute(
            """
            SELECT vacancy_name FROM vacancies
            WHERE vacancy_name ILIKE %s
        """,
            (f"%{keyword}%",),
        )
        vacancies = self.cursor.fetchall()
        return [vacancy[0] for vacancy in vacancies]
