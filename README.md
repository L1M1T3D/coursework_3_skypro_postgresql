Напишите скрипт на Python, который:

Подключается к базе данных PostgreSQL;

Создает таблицы в базе данных:

Таблица customers должна содержать следующие столбцы - customer_id (строка 5 символов), company_name (строка до 100 символов), contact_name (строка до 100 символов). Все поля являются обязательными.

Таблица employees должна содержать следующие столбцы - employee_id (целое число), first_name (строка до 25 символов), last_name (строка до 35 символов), title (строка до 100 символов), birth_date (дата), notes (текст). Обязательные для заполнения поля - все, кроме поля notes.

Таблица orders должна содержать следующие столбцы - order_id (целое число), customer_id (ссылка на поле customer_id таблицы customers), employee_id (ссылка на поле employee_id таблицы employees), order_date (дата), ship_city (строка до 100 символов). Все поля являются обязательными.

Выполняет операцию вставки данных из списков customers_data, employees_data, ordres_data в таблицы customers, employees, orders соответственно.