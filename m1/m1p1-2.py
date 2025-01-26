def luhns(card_nbr):
    def luhn_sum(digits):
        sum = 0
        for index, digit in enumerate(reversed(digits)):
            if index % 2 == 0:  # even
                sum += digit
            else:
                doubled = digit * 2
                sum += (
                    doubled if doubled < 10 else doubled - 9
                )  # we just count digits not the numbers
        return sum

    x_index = card_nbr.index("X")

    digits = [int(d) if d.isdigit() else 0 for d in card_nbr]

    for x in range(10):
        digits[x_index] = x
        if luhn_sum(digits) % 10 == 0:
            return x


def find_x_in_cards(card_numbers):
    print("luhns algorithm with:\n")
    for i in card_numbers:
        print(i)
    result = ""
    for card_number in card_numbers:
        censored_digit = luhns(card_number)
        result += str(censored_digit)
    print("\nresult:", result, "\n")
    return result


def luhns(card_nbr):
    def luhn_sum(digits):
        sum = 0
        for index, digit in enumerate(reversed(digits)):
            if index % 2 == 0:  # even
                sum += digit
            else:
                doubled = digit * 2
                sum += (
                    doubled if doubled < 10 else doubled - 9
                )  # we just count digits not the numbers
        return sum

    x_index = card_nbr.index("X")

    digits = [int(d) if d.isdigit() else 0 for d in card_nbr]

    for x in range(10):
        digits[x_index] = x
        if luhn_sum(digits) % 10 == 0:
            return x


def find_x_in_cards(card_numbers):
    print("luhns algorithm with:\n")
    for i in card_numbers:
        print(i)
    result = ""
    for card_number in card_numbers:
        censored_digit = luhns(card_number)
        result += str(censored_digit)
    print("\nresult:", result, "\n")
    return result


card_numbers = [
    "12774212857X4109",
    "586604X108627571",
    "7473X86953606632",
    "4026467X45830632",
    "20X3092648604969",
]
find_x_in_cards(card_numbers)
