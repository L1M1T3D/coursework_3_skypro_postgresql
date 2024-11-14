from typing import Any, Dict, List

import psycopg2


def create_database(database_name: str, params: Dict[str, str]) -> None:
    """Создает базу данных."""
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")
    conn.close()


def create_tables(database_name: str, params: Dict[str, str]) -> None:
    """Создает таблицы в базе данных."""
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        # Создание таблицы работодателей
        cur.execute(
            """
            CREATE TABLE employers (
                id SERIAL PRIMARY KEY,
                employer_id VARCHAR UNIQUE,
                employer_name VARCHAR NOT NULL,
                url VARCHAR NOT NULL,
                open_vacancies INTEGER
            )
        """
        )

        # Создание таблицы вакансий
        cur.execute(
            """
            CREATE TABLE vacancies (
                id SERIAL PRIMARY KEY,
                vacancy_id VARCHAR UNIQUE,
                employer_id INTEGER REFERENCES employers(id),
                vacancy_name VARCHAR NOT NULL,
                salary_from INTEGER,
                salary_to INTEGER,
                currency VARCHAR(7),
                published_at DATE,
                url VARCHAR NOT NULL,
                prof_role VARCHAR,
                employment VARCHAR
            )
        """
        )
    conn.commit()
    conn.close()


def save_data_to_db(
    database_name: str,
    params: Dict[str, str],
    vacancies_data: List[Dict[str, Any]],
    employers_data: List[Dict[str, Any]],
) -> None:
    """Добавляет вакансии и работодателей в соответствующие таблицы."""
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        # Вставка данных о работодателях
        for employer in employers_data:
            cur.execute(
                """
                INSERT INTO employers (employer_id, employer_name, url, open_vacancies)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (employer_id) DO NOTHING
                RETURNING id
            """,
                (employer["id"], employer["name"], employer["alternate_url"], employer["open_vacancies"]),
            )

            employer_id = cur.fetchone()[0] if cur.rowcount > 0 else None

            # Вставка данных о вакансиях, связанных с работодателем
            if employer_id:
                for vacancy in vacancies_data:
                    if vacancy["salary"]:
                        salary_from = vacancy["salary"].get("from")
                        salary_to = vacancy["salary"].get("to")
                        currency = vacancy["salary"].get("currency")
                    else:
                        salary_from, salary_to, currency = None, None, None

                    cur.execute(
                        """
                        INSERT INTO vacancies (vacancy_id, employer_id, vacancy_name,
                        salary_from, salary_to, currency, published_at, url, prof_role, employment)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (vacancy_id) DO NOTHING
                    """,
                        (
                            vacancy["id"],
                            employer_id,
                            vacancy["name"],
                            salary_from,
                            salary_to,
                            currency,
                            vacancy["published_at"],
                            vacancy["alternate_url"],
                            vacancy["professional_roles"][0]["name"],
                            vacancy["employment"]["name"],
                        ),
                    )
    conn.commit()
    conn.close()
