from collections import defaultdict

# Грамматика в нормальной форме Хомского
grammar = {
    'S': ['VA'],
    'A': ['QE'],

    'E': [
        'EX', 'EY', 'MZ', 'MW', 'RU', 'OC',
        'a', 'b', 'c', 'd', 'e', 'f', '0', '1', 'BN'
    ],

    'M': [
        'MZ', 'MW', 'RU', 'OC',
        'a', 'b', 'c', 'd', 'e', 'f', '0', '1', 'BN'
    ],

    'U': [
        'RU', 'OC',
        'a', 'b', 'c', 'd', 'e', 'f', '0', '1', 'BN'
    ],

    'X': ['PM'],
    'Y': ['RM'],
    'Z': ['TU'],
    'W': ['DU'],
    'C': ['EH'],

    'N': ['BN', '0', '1'],
    'B': ['0', '1'],

    'V': ['a', 'b', 'c', 'd', 'e', 'f'],

    'Q': ['='],
    'P': ['+'],
    'R': ['-'],
    'T': ['*'],
    'D': ['/'],
    'O': ['('],
    'H': [')']
}


terminal_rules = defaultdict(set)
binary_rules = defaultdict(set)

for left, productions in grammar.items():
    for right in productions:
        if len(right) == 1:
            terminal_rules[right].add(left)
        elif len(right) == 2:
            binary_rules[right].add(left)


def cyk(word):
    n = len(word)

    if n == 0:
        return False

    table = [[set() for _ in range(n)] for _ in range(n)]

    for i in range(n):
        if word[i] not in terminal_rules:
            return False

        table[i][i] = terminal_rules[word[i]].copy()

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            for k in range(i, j):
                for left in table[i][k]:
                    for right in table[k + 1][j]:
                        pair = left + right

                        if pair in binary_rules:
                            table[i][j].update(binary_rules[pair])

    return 'S' in table[0][n - 1]


# Тестовые цепочки
tests = [
    'a=1',
    'b=10+1',
    'c=a+b*10',
    'd=-(a+1)',
    'e=a/b',
    'f=1-0/1',
    'a=(b-c)*10',
    'g=1',
    'a=2',
    'a=1+',
    'a=(1+0',
    'a=1**0'
]

print("Результаты распознавания методом CYK:\n")

for i, word in enumerate(tests, start=1):
    result = "Accept" if cyk(word) else "Reject"
    print(f"{i}. {word:10} - {result}")