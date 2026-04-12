import ast


def parse_file(path: str):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        source = f.read()

    try:
        return ast.parse(source)

    except SyntaxError as e:

        # Фикс частой ошибки OWASP Benchmark:
        # вложенные кавычки в f-string
        fixed = source.replace("decode('utf-8')", 'decode("utf-8")')

        try:
            return ast.parse(fixed)
        except SyntaxError:
            return None