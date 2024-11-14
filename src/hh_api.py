from typing import Any, Dict, List
import requests


class HHApi:
    """
    Получает данные о работодателях и их вакансиях с hh.ru.
    """

    def __init__(self) -> None:
        self.url_vacancies = "https://api.hh.ru/vacancies"
        self.url_employers = "https://api.hh.ru/employers"

    def get_vacancies_by_employer(self, employer_id: str, page: int = 0, per_page: int = 50) -> List[Dict[str, Any]]:
        """
        Метод для получения вакансий по работодателю.
        """
        params = {"employer_id": employer_id, "page": page, "per_page": per_page}
        response = requests.get(self.url_vacancies, params=params)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            raise Exception("Ошибка при получении данных с hh.ru")

    def get_employers(self, employers_list: List[str]) -> List[Dict[str, Any]]:
        """
        Метод для получения работодателей.
        """
        result = []
        for employer in employers_list:
            employer_id = f"{self.url_employers}/{int(employer)}"
            response = requests.get(employer_id)
            if response.status_code == 200:
                result.append(response.json())
            else:
                raise Exception("Ошибка при получении данных с hh.ru")
        return result
