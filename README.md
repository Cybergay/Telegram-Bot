## Описание проекта

Это бот для управления и отображения расписания университета, который я разработал с нуля. Бот использует собственную базу данных на **PostgreSQL**, где хранится информация о расписаниях занятий, преподавателях и аудиториях. Он создан для того, чтобы помочь студентам и преподавателям легко получать актуальную информацию о занятиях.

## Функции бота

- **Запрос расписания**: студенты могут получить расписание на любой день недели.
- **Фильтрация по группам, преподавателям и аудиториям**: бот может отображать расписание для конкретной учебной группы или аудитории.
- **Управление через админ-панель**: поддержка CRUD операций для администраторов для добавления и редактирования информации.
- **Уведомления об изменениях**: бот может уведомлять студентов и преподавателей об изменениях в расписании.
- **Интеграция с базой данных**: собственная база данных на **PostgreSQL** обеспечивает высокую скорость работы и гибкость при хранении данных.

## Используемые технологии

- **Python**: основной язык программирования для разработки бота.
- **PostgreSQL**: база данных для хранения расписания и другой информации.
- **SQLAlchemy**: ORM для работы с базой данных.
- **Telegram API**: интерфейс взаимодействия бота с пользователями.
- **Docker** (опционально): для удобного разворачивания и контейнеризации приложения.
