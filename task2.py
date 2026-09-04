from itertools import combinations


def lucky_ticket(digits: tuple[int, ...]): #наполняемый кортеж
    """Проверяет, можно ли составить счастливый билет из шести цифр."""

    if len(digits) != 6:
        raise ValueError("Передаем ровно шесть цифр")

    for digit in digits:
        if digit < 0 or digit > 9:
         raise ValueError(
                "Элемент кортежа должен быть цифрой от 0 до 9"
            )

    total_sum = sum(digits)

    if total_sum % 2 != 0:
        return False

    half_sum = total_sum // 2

    for first_half in combinations(digits, 3):
        if sum(first_half) == half_sum:
            return True
    return False


if __name__ == "__main__":
    ticket = (1, 2, 8, 9, 4, 1)

    if lucky_ticket(ticket):
        print("Из этих цифр можно составить счастливый билет")
    else:
        print("Из этих цифр нельзя составить счастливый билет")
