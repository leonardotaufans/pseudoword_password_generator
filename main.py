import random
import re


def split_syllables_from_letters(letters, arrange):
    consonant_index = re.search('vc{2,}', arrange)
    while consonant_index:
        i = consonant_index.start() + 1
        letters = letters[:i + 1] + ['|'] + letters[i + 1:]
        arrange = arrange[:i + 1] + '|' + arrange[i + 1:]
        consonant_index = re.search('vc{2,}', arrange)

    vocal_index = re.search(r'v{2,}', arrange)
    while vocal_index:
        i = vocal_index.start()
        letters = letters[:i + 1] + ['|'] + letters[i + 1:]
        arrange = arrange[:i + 1] + '|' + arrange[i + 1:]
        vocal_index = re.search(r'v{2,}', arrange)

    vcv_index = re.search(r'vcv', arrange)
    while vcv_index:
        i = vcv_index.start()
        letters = letters[:i + 1] + ['|'] + letters[i + 1:]
        arrange = arrange[:i + 1] + '|' + arrange[i + 1:]
        vcv_index = re.search(r'vcv', arrange)

    sep_index = re.search(r'[cvs]s', arrange)
    while sep_index:
        i = sep_index.start()
        letters = letters[:i + 1] + ['|'] + letters[i + 1:]
        arrange = arrange[:i + 1] + '|' + arrange[i + 1:]
        sep_index = re.search(r'[cvs]s', arrange)

    sep_index = re.search(r's[cvs]', arrange)
    while sep_index:
        i = sep_index.start()
        letters = letters[:i + 1] + ['|'] + letters[i + 1:]
        arrange = arrange[:i + 1] + '|' + arrange[i + 1:]
        sep_index = re.search(r's[cvs]', arrange)

    return ''.join(letters).split('|')


class SyllableSplitter:

    def __init__(self, consonant=None, vocal=None, double_consonant=None):
        self.consonant = ['b', 'c', 'd', 'f', 'g', 'h', 'j',
                          'k', 'l', 'm', 'n', 'p', 'q', 'r',
                          's', 't', 'v', 'w', 'x', 'y', 'z',
                          'ng', 'ny', 'sy', 'ch', 'dh', 'gh',
                          'kh', 'ph', 'sh', 'th'] + (consonant or [])

        self.double_consonant = ['ll', 'ks', 'rs', 'rt'] + (double_consonant or [])

        self.vocal = ['a', 'e', 'i', 'o', 'u'] + (vocal or [])

    def split_letters(self, string):
        letters = []
        arrange = []

        while string != '':
            letter = string[:2]

            if letter.lower() in self.double_consonant:

                if string[2:] != '' and string[2].lower() in self.vocal:
                    letters += [letter[0]]
                    arrange += ['c']
                    string = string[1:]

                else:
                    letters += [letter]
                    arrange += ['c']
                    string = string[2:]

            elif letter.lower() in self.consonant:
                letters += [letter]
                arrange += ['c']
                string = string[2:]

            elif letter.lower() in self.vocal:
                letters += [letter]
                arrange += ['v']
                string = string[2:]

            else:
                letter = string[0]

                if letter.lower() in self.consonant:
                    letters += [letter]
                    arrange += ['c']
                    string = string[1:]

                elif letter.lower() in self.vocal:
                    letters += [letter]
                    arrange += ['v']
                    string = string[1:]

                else:
                    letters += [letter]
                    arrange += ['s']
                    string = string[1:]

        return letters, ''.join(arrange)

    def split_syllables(self, string):
        letters, arrange = self.split_letters(string)
        return split_syllables_from_letters(letters, arrange)


def get_random_word_dictionary():
    try:
        file = open('dictionary.txt')
        line = next(file)
        for num, aline in enumerate(file, 2):
            if random.randrange(num):
                continue
            line = aline
        return line
    except FileNotFoundError as e:
        print('Dictionary file missing!')
        exit(-1)
    except Exception:
        print('General exception occurred.')
        exit(-1)


def randomly_uppercase_letters(word: str):
    result = ""
    p: str
    for p in word:
        if random.choice([True, False, False, False, False]):  # Minimizing uppercase
            result += p.upper()
        else:
            result += p
    return result


def get_pseudo_word(length: int):
    pseudo_word: list = []
    length_syllable = round(length / 2)
    current_syllable = 0
    while True:
        print(f"loop {current_syllable + 1}")
        word_pre_validated = get_random_word_dictionary()
        # print(word_pre_validated)
        if len(
                word_pre_validated) < 4: continue  # Length should have the minimum of 4 word to be supported by get syllables
        if word_pre_validated[0] == word_pre_validated[
            1]: continue  # To prevent any double letter at the start (aa, ee, oo)
        splitter = SyllableSplitter()
        syllables: list = splitter.split_syllables(word_pre_validated)
        # syllables: list = get_syllables(word_pre_validated)
        if len(syllables) <= current_syllable: continue
        if len(syllables[current_syllable]) <= 2: continue
        pseudo_word.append(syllables[current_syllable])
        current_syllable = current_syllable + 1
        if current_syllable >= length_syllable:
            break
    result = randomly_uppercase_letters("".join(pseudo_word))

    return result


def random_with_n_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return random.randint(range_start, range_end)


symbols = ["@", "#", "$", "_", "&", "-", "+", "(", ")", "/", "*", "'", ":", ";", "!", "?"]

if __name__ == "__main__":
    password = (f"{get_pseudo_word(random.randint(4, 6)).capitalize()}{random.choice(symbols)}"
                f"{random_with_n_digits(random.randint(4, 6))}{random.choice(symbols)}"
                f"{get_pseudo_word(random.randint(4, 6)).capitalize()}{random.choice(symbols)}")
    print(password)
