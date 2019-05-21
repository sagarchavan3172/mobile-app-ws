import math
OPERATORS = set(['+', '-', '*', '/', '(', ')'])

def signFunc(c):
    if c > 0:
        return 1
    return -1

def orderOperator(c):
    if c == '+' or c == '-':
        return 1
    if c == '*' or c == '/':
        return 2
    return 0

def calculate(first, second, c):
    answer = 0
    if c == '+':
        answer = first + second
    elif c == '-':
        answer = first - second
    elif c == '*':
        answer = first * second
    else:
        #check two value's sign is same or different.
        sign = signFunc(first) * signFunc(second)
        if sign == 1:
            answer = math.floor((math.fabs(first) - 1) / math.fabs(second))
            answer = answer + 1
        else:
            answer = -1 * math.floor((math.fabs(first) / math.fabs(second)))
    if answer < -128 or answer >= 127 :
        raise Exception('value should not exceed range. The value was: {}'.format(answer))
    return answer

def convertInt(val):
    con_val = int(val)
    if con_val < -128 or con_val >= 127 :
        raise Exception('value should not exceed range. The value was: {}'.format(con_val))
    return con_val

def infix_to_prefix(infix):
    op_stack = []
    val_stack = []
    prefix_stack = []
    previous = '('
    val = ''
    for ch in infix:
        if not ch in OPERATORS:
            previous = ch
            val = val + ch
            continue

        if val != '':

            val_stack.append(convertInt(val))
            prefix_stack.append(val)
            val = ''

        if ch == '(':
            op_stack.append(ch)
        elif ch == ')':
            while op_stack[-1] != '(':
                op = op_stack.pop()
                first = prefix_stack.pop()
                firstVal = val_stack.pop()
                if op == '^':
                    val_stack.append(-firstVal)
                    prefix_stack.append('^' + first)
                    continue
                second = prefix_stack.pop()
                secondVal = val_stack.pop()
                val_stack.append(calculate(secondVal, firstVal, op))
                prefix_stack.append( op + second + first )
            op_stack.pop() # pop '('
        else:
            if(ch == '-' and previous == '('):
                previous = ch
                op_stack.append('^')
                continue
            while op_stack and op_stack[-1] != '(' and orderOperator(ch) <= orderOperator(op_stack[-1]):
                op = op_stack.pop()
                first = prefix_stack.pop()
                firstVal = val_stack.pop()
                if op == '^':
                    val_stack.append(-firstVal)
                    prefix_stack.append('^' + first)
                    continue
                second = prefix_stack.pop()
                secondVal = val_stack.pop()
                val_stack.append(calculate(secondVal, firstVal, op))
                prefix_stack.append( op + second + first )
            op_stack.append(ch)
        previous = ch
    if val != '':
        val_stack.append(convertInt(val))
        prefix_stack.append(val)
    # leftover
    while op_stack:
        op = op_stack.pop()
        first = prefix_stack.pop()
        firstVal = val_stack.pop()
        if op == '^':
            val_stack.append(-firstVal)
            prefix_stack.append('^' + first)
            continue
        second = prefix_stack.pop()
        secondVal = val_stack.pop()
        val_stack.append(calculate(secondVal, firstVal, op))
        prefix_stack.append( op + second + first )

    return {'prefix': prefix_stack[-1], 'value': val_stack[-1]}

if __name__ == '__main__':
    #infix_to_postfix('1+(3+4*6+6*1)*2/3')
    #prefix = infix_to_prefix('-(-100)')
    result = infix_to_prefix('101*61')
    print(result['prefix'])
    print(result['value'])


