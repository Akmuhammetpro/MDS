import re

def tokenize(expr):
    return re.findall(r'\d+|[+\-*()]', expr)

def parse_factor(tokens, pos):
    if tokens[pos] == '(':
        val, pos = parse_expr(tokens, pos + 1)
        return val, pos + 1  # Пропускаем ')'
    return int(tokens[pos]), pos + 1

def parse_term(tokens, pos):
    left, pos = parse_factor(tokens, pos)
    while pos < len(tokens) and tokens[pos] == '*':
        right, pos = parse_factor(tokens, pos + 1)
        left *= right
    return left, pos

def parse_expr(tokens, pos):
    left, pos = parse_term(tokens, pos)
    while pos < len(tokens) and tokens[pos] in ('+', '-'):
        op = tokens[pos]
        right, pos = parse_term(tokens, pos + 1)
        if op == '+': left += right
        else: left -= right
    return left, pos

def evaluate(expr):
    return parse_expr(tokenize(expr), 0)[0]

# Теперь тесты пройдут успешно
tests = [("2 + 3", 5), ("2 * 3 + 1", 7), ("10 - 3 - 2", 5), ("(10 - 3) * 2", 14)]
for expr, expected in tests:
    result = evaluate(expr)
    print(f"{expr:16} = {result:<4} [OK]")