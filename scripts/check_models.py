import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import inspect
from bank_api.db.base import Base
from bank_api.db.engine import engine
from bank_api.db.tables import account, credit, transactions, user  # noqa: F401


def main() -> None:
    inspector = inspect(engine)
    real_tables = set(inspector.get_table_names())

    if not Base.metadata.tables:
        print("В Base.metadata нет ни одной таблицы. Проверь импорты.")
        return

    problems = 0
    for table_name, table in sorted(Base.metadata.tables.items()):
        if table_name not in real_tables:
            print(f"[{table_name}] таблицы нет в базе")
            problems += 1
            continue

        in_db = {column["name"] for column in inspector.get_columns(table_name)}
        in_model = {column.name for column in table.columns}

        only_model = in_model - in_db
        only_db = in_db - in_model

        if only_model or only_db:
            problems += 1
            print(f"[{table_name}]")
            if only_model:
                print(f"    в модели есть, в базе нет : {', '.join(sorted(only_model))}")
            if only_db:
                print(f"    в базе есть, в модели нет : {', '.join(sorted(only_db))}")

    print(f"\nПроверено таблиц: {len(Base.metadata.tables)}. "
          f"{'Расхождений нет.' if problems == 0 else f'С расхождениями: {problems}.'}")

    engine.dispose()


if __name__ == "__main__":
    main()
