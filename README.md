# time-tracking-skillbox

## Описание

Итоговая работа в рамках курса «Базы данных для разработчиков».

Примеры файлов с данными в *data/*

Концептуальная/логическая/физическая модели БД в файле *time_tracking_skillbox.drawio*

## Настройка
1. Склонировать проект, перейти в рабочий каталог
   * `git clone https://github.com/DaaN1L/time-tracking-skillbox.git`
   * `cd time-tracking-skillbox`
3. Создать и активировать виртуальное окружение
   * `python -m venv .env`
   * `source .env/bin/activate`
4. Установить зависимости
   * `pip install -r requirements.txt`
  
Дополнительно требуется поднятый инстанс БД MySQL.
Креды и endpoint для подключения к БД указать в файле *.env*

Скрипты для создания объектов БД в *mysql/schema.sql*


## Использование

`python main.py --help` — список команд верхнего уровня

* `python main.py import <POSITIONS_PATH.csv>` — добавить в БД указанных в файле *POSITIONS_PATH.csv* должности и ставки оплаты труда;
* `python main.py import <EMPLOYEES_PATH.csv>` — добавить в БД указанных в файле *EMPLOYEES_PATH.csv* должности и ФИО сотрудников;
* `python main.py import <TIMESHEET_PATH.csv>` — добавить в БД указанных в файле *TIMESHEET_PATH.csv* периоды работы сотрудников над задачами;
* `python main.py list employee` — выводит и перечисляет всех сотрудников по именам;
* `python main.py get <EMPLOYEE_NAME>` — выводит timesheet сотрудника по его имени;
* `python main.py remove <EMPLOYEE_NAME>` — удаляет данные по сотруднику из timesheet по его имени;
* `python main.py report top5longTasks` — выводит пять задач, на которые потрачено больше всего времени;
* `python main.py report top5costTasks` — выводит пять задач, на которые потрачено больше всего денег;
* `python main.py report top5employees` — выводит пять сотрудников, отработавших наибольшее количество времени за всё время.


---
Python 3.10.11
