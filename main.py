import os
import csv
import argparse
from tabulate import tabulate


class CSV:
    CSV_FILE = "my_data.csv"
    COLUMNS = ["name", "brand", "price", "rating"]

    def read_data_from_csv_file(self, file_path: str) -> list[dict[str, str]]:
        try:
            with open(file_path, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                data = list(reader)
                return data
        except FileNotFoundError:
            raise FileNotFoundError(f"Файла {file_path} не существует")

    def add_data_to_csv_file(
        self, name: str, brand: str, price: float, rating: float
    ) -> None:

        new_entry = {"name": name, "brand": brand, "price": price, "rating": rating}
        file_exists = os.path.isfile(self.CSV_FILE)

        with open(self.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.COLUMNS)
            if not file_exists:
                writer.writeheader()
            writer.writerow(new_entry)

    def filter_data(
        self, data: list[dict[str, str]], column: str, value: str
    ) -> list[dict[str, str]]:
        if not data:
            return []
        if not data or column not in data[0]:
            raise ValueError(f"Колонкa {column} для фильтрации не найдена")
        filtered_results = []
        for item in data:
            if item.get(column) == str(value):
                filtered_results.append(item)
        return filtered_results

    def aggregate_data(
        self, data: list[dict[str, str]], column: str, operation: str
    ) -> list[dict[str, str]]:

        if column not in data[0]:
            raise KeyError(f"Колонка '{column}' не существует в данных для агрегации.")

        try:
            item = [float(item[column]) for item in data]
        except ValueError as e:
            raise ValueError(
                f"Невозможно аггрегировать колонку {column}. Данные не являются числами {e}"
            )

        if operation == "min":
            return min(item)
        elif operation == "max":
            return max(item)
        elif operation == "avg":
            return sum(item) / len(item)
        elif operation == "sum":
            return sum(item)
        else:
            raise ValueError(f"Неизвестная операция для аггрегации {operation}")

    def print_data(self, data: list[dict[str, str]]) -> None:
        if not data:
            print("Нет данных для отображения")
            return
        print(tabulate(data, headers="keys", tablefmt="grid"))


def parse_arguments() -> None:
    parser = argparse.ArgumentParser(description="Обработчик CSV файлов")
    parser.add_argument(
        "--file", required=True, help="Имя CSV файла"
        )
    parser.add_argument(
        "--where", help='Условие для фильтрации, пример "price<1500.00'
        )
    parser.add_argument(
        "--aggregate", help="Колонка для аггрегации данных"
        )

    return parser.parse_args()


def filter_parse_args(condition: str) -> tuple[str, str, str]:
    if ">=" in condition:
        column, value = condition.split(">=")
        operator = ">="
    elif "<=" in condition:
        column, value = condition.split("<=")
        operator = "<="
    
    elif ">" in condition:
        column, value = condition.split(">")
        operator = ">"
    elif "<" in condition:
        column, value = condition.split("<")
        operator = "<"

    elif "=" in condition:
        column, value = condition.split("=")
        operator = "="
    else:
        raise ValueError("Некорректное условие для фильтрации")
    return column.strip(), operator, value.strip()


def aggregate_parse_args(condition: str) -> tuple[str, str]:
    if "=" not in condition:
        raise ValueError("Некорректное условие для аггрегации")
    column, operation = condition.split("=")
    return column.strip(), operation.strip()


def main() -> None:
    args = parse_arguments()
    my_csv = CSV()
    data = []
    
    data = my_csv.read_data_from_csv_file(args.file)

    if args.where:
        column, operator, value = filter_parse_args(args.where)
        
        if operator == ">=":
            data = [item for item in data if float(item[column]) >= float(value)]
        elif operator == "<=":
            data = [item for item in data if float(item[column]) <= float(value)]
        elif operator == "=":
            data = my_csv.filter_data(data, column, value.lower())
        elif operator == ">":
            data = [item for item in data if float(item[column]) > float(value)]
        elif operator == "<":
            data = [item for item in data if float(item[column]) < float(value)]
       

    if args.aggregate:
        column, operation = aggregate_parse_args(args.aggregate)
        result = my_csv.aggregate_data(data, column, operation)
        print(tabulate([[result]], headers=[operation], tablefmt="grid"))
        return
    else:
        my_csv.print_data(data)


if __name__ == "__main__":
    main()
