import re


def try_int(exp):
    if type(exp) == float:
        if exp.is_integer():
            return int(exp)
    return exp


def try_float(exp):
    exp = exp.strip()
    try:
        return float(exp)
    except ValueError:
        return exp


def get_mult(exp):
    mult_match = re.search(r'(.*)\s*([\*\/])\s*(.*)', exp)
    if mult_match:
        operand = mult_match.group(2)
        var1, var2 = mult_match.group(1), mult_match.group(3)
        if operand == '*':
            exp = exp.replace(mult_match.group(), str(go_by_order(var1) * go_by_order(var2)))
        elif operand == '/':
            try:
                exp = exp.replace(mult_match.group(), str(go_by_order(var1) / go_by_order(var2)))
            except ZeroDivisionError:
                raise ZeroDivisionError('You divided by zero. Oops')
    return exp


def get_basic(exp):
    basic_match = re.search(r'(.*)\s*([\+\-])\s*(.*)', exp)
    if basic_match:
        operand = basic_match.group(2)
        var1, var2 = basic_match.group(1), basic_match.group(3)
        if operand == '+':
            exp = exp.replace(basic_match.group(), str(go_by_order(var1) + go_by_order(var2)))
        elif operand == '-':
            exp = exp.replace(basic_match.group(), str(go_by_order(var1) - go_by_order(var2)))
        else:
            raise TypeError('unrecognized operator')
    return exp


def get_power(exp):
    power_match = re.search(r'(.*)\s*\^\s*(.*)', exp)
    if power_match:
        var1, var2 = power_match.group(1), power_match.group(2)
        exp = exp.replace(power_match.group(), str(go_by_order(var1) ** go_by_order(var2)))
    return exp


def get_brackets(exp):
    bracket_match = re.search(r'\((.+)\)', exp)
    if bracket_match:
        exp = exp.replace(bracket_match.group(), str(go_by_order(bracket_match.group(1))))
    return exp


def go_by_order(exp):
    exp = try_float(exp)
    if type(exp) == str:
        exp = get_brackets(exp)
        exp = get_basic(exp)
        exp = get_mult(exp)
        exp = get_power(exp)
        exp = try_float(exp)
    return try_int(exp)


def is_illegal_char(exp):
    if re.search(r'[^\d\+\-\*\/\^\(\)\s]', exp):
        print('illegal characters detected')
        return True
    pass


def main():
    while True:
        expression = input("Calculate whatever you want! ")
        if expression == '0':
            break
        if is_illegal_char(expression):
            continue
        print(go_by_order(expression))


if __name__ == '__main__':
    main()
