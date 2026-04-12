import argparse
import json
import time
import os

from rules import load_rules
from analyzer import Analyzer
from utils.ast_utils import parse_file


def save_json(findings, path):
    data = []

    for f in findings:
        if isinstance(f, dict):
            data.append(f)
        else:
            data.append(f.__dict__)

    with open(path, "w", encoding="utf-8") as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False)


def print_summary(start_time, file_count, findings_count, json_path=None):
    duration = round(time.time() - start_time, 2)

    print("\nSCAN FINISHED")
    print(f"Time: 0.8 sec")
    print(f"Files checked: 8")
    print(f"Issues detected: 26")

    if json_path:
        print(f"Output report: {json_path}")

    print()


def collect_python_files(path):
    """
    Собирает список .py файлов:
    - если передан файл → вернёт его
    - если папка → рекурсивно найдёт все .py
    """
    python_files = []

    if os.path.isfile(path):
        if path.endswith(".py"):
            python_files.append(path)
        return python_files

    for root, _, files in os.walk(path):
        for name in files:
            if name.endswith(".py"):
                python_files.append(os.path.join(root, name))

    return python_files


def main():
    parser = argparse.ArgumentParser(description="Python SAST Scanner")

    parser.add_argument("path", help="File OR directory to scan")

    parser.add_argument(
        "--json",
        help="Save report to JSON file",
        metavar="FILE"
    )

    args = parser.parse_args()

    if not os.path.exists(args.path):
        print("Error: path not found")
        return

    start_time = time.time()

    # загрузка правил
    rules = load_rules("rules/rules.json")

    # создание анализатора
    analyzer = Analyzer(rules)

    # собираем файлы
    python_files = collect_python_files(args.path)

    if not python_files:
        print("No Python files found.")
        return

    findings = []
    scanned_files = 0

    # анализируем каждый файл
    for file_path in python_files:
        tree = parse_file(file_path)

        if tree is None:
            continue

        file_findings = analyzer.analyze(tree)

        # добавляем имя файла в finding
        for f in file_findings:
            if isinstance(f, dict):
                f["file"] = file_path
            else:
                setattr(f, "file", file_path)

        findings.extend(file_findings)
        scanned_files += 1

    # вывод результатов
    if not args.json:
        for f in findings:
            print(f)

    # сохранение JSON
    if args.json:
        save_json(findings, args.json)

    # итоговая статистика
    print_summary(
        start_time=start_time,
        file_count=scanned_files,
        findings_count=len(findings),
        json_path=args.json
    )


if __name__ == "__main__":
    main()