"""Полный сброс тестовой базы.

Сносит все данные приложения физически (не мягким удалением, как это делает API)
и заново создаёт админа. После сброса у админа id = 1, следующая запись получит id = 2.

Таблица doctrine_migration_versions не трогается.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import create_engine, text

from bank_api.config import settings

# Порядок для вывода. В TRUNCATE порядок не важен — CASCADE разберётся со связями.
TABLES = ("user", "account", "transaction", "credit")


def show_state(conn, title: str) -> None:
    print(f"\n{title}")
    for table in TABLES:
        count = conn.execute(text(f'SELECT count(*) FROM "{table}"')).scalar()
        print(f"  {table:14} строк: {count}")
    for name, last_value in conn.execute(text("""
            SELECT sequencename, last_value FROM pg_sequences
            WHERE schemaname = 'public' ORDER BY sequencename""")):
        print(f"  {name:22} last_value: {last_value}")


def main() -> None:
    engine = create_engine(settings.db_url)

    # 1. Смотрим, что есть, и забираем данные админа до сноса
    with engine.connect() as conn:
        show_state(conn, "ДО сброса:")

        admin = conn.execute(text("""
            SELECT username, password, role FROM "user"
            WHERE username = :username AND deleted_at IS NULL
            ORDER BY id LIMIT 1"""), {"username": settings.admin_username}).fetchone()

    if admin is None:
        print(f"\nАдмин '{settings.admin_username}' в базе не найден. Прерываю, "
              f"иначе после сброса некому будет заходить.")
        engine.dispose()
        return

    # 2. Спрашиваем подтверждение вне транзакции, чтобы не держать её открытой
    print(f"\nБудут физически удалены ВСЕ строки из: {', '.join(TABLES)}")
    print(f"Админ '{admin.username}' будет создан заново с id = 1.")
    if input('Продолжить? Напиши "да": ').strip().lower() != "да":
        print("Отменено, ничего не изменилось.")
        engine.dispose()
        return

    # 3. Сносим и восстанавливаем админа
    with engine.begin() as conn:
        conn.execute(text('TRUNCATE "transaction", "credit", "account", "user" '
                          'RESTART IDENTITY CASCADE'))
        conn.execute(text("""
            INSERT INTO "user" (username, password, role)
            VALUES (:username, :password, :role)"""),
                     {"username": admin.username,
                      "password": admin.password,
                      "role": admin.role})

    # 4. Показываем результат
    with engine.connect() as conn:
        show_state(conn, "ПОСЛЕ сброса:")
        admin_id = conn.execute(text('SELECT id FROM "user" WHERE username = :username'),
                                {"username": settings.admin_username}).scalar()
        print(f"\nГотово. Админ восстановлен с id = {admin_id}, "
              f"следующая запись получит id = {admin_id + 1}.")

    engine.dispose()


if __name__ == "__main__":
    main()
