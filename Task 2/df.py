import random

P = 124325339146889384540494091085456630009856882741872806181731279018491820800119460022367403769795008250021191767583423221479185609066059226301250167164084041279837566626881119772675984258163062926954046545485368458404445166682380071370274810671501916789361956272226105723317679562001235501455748016154805420913

G = 1399252811935680595399801714158014275474696840019

def is_prime(n, k=5):
    if n <= 1 or n % 2 == 0:
        return False

    # Выразим n - 1 как 2^s * d
    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    # Проводим k итераций теста Миллера-Рабина
    for _ in range(k):
        a = random.randint(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

def generate_prime(bits):
    while True:
        candidate = random.getrandbits(bits)
        # Убедимся, что число нечетное и простое
        if candidate % 2 == 1 and is_prime(candidate):
            return candidate

if __name__ == "__main__":
    # Пример использования: генерация простого числа с 256 битами
    prime_number = generate_prime(256)
    print("Сгенерированное простое число:", prime_number)