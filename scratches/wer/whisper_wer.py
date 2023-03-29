import whisper
import json
import re
import pymorphy2
import os.path
from jiwer import wer
from spellchecker import SpellChecker

path_sound = '/opt/scripts/whisper_example/scratches/wer/sounds/'
json_file_path = r'file_text.json'
result = []


def transcribe_file(name: str, model, language: str):
    decode_options = dict(language=language, fp16=True)
    transcribe_options = dict(task="transcribe", **decode_options)
    try:
        transcription = model.transcribe(name, **transcribe_options)
    except RuntimeError:
        print(f'ERROR in file {name}')
        return 'Null'
    return transcription["text"]


def word_number2number(text: str):
    morph = pymorphy2.MorphAnalyzer()

    text = f' {text.lower()} '

    text = re.sub("миллион[а-я]?[а-я]?[а-я]?", "1000000##", text)

    text = re.sub("тысяч[а-я]?[а-я]?[а-я]?", "1000##", text)

    hundreds = {100: 'сто', 200: 'двести', 300: 'триста', 400: 'четыреста', 500: 'пятьсот',
                600: 'шестьсот', 700: 'семьсот', 800: 'восемьсот', 900: 'девятьсот'}
    for num in hundreds.keys():
        test = morph.parse(hundreds[num])[0]
        lexeme = test.lexeme
        for lex in lexeme:
            text = text.replace(f' {lex.word} ', f" {num}## ")

    dozens = {10: 'десять', 20: 'двадцать', 30: 'тридцать', 40: 'сорок', 50: 'пятьдесят',
              60: 'шестьдесят', 70: 'семьдесят', 80: 'восемьдесят', 90: 'девяносто'}
    for num in dozens.keys():
        test = morph.parse(dozens[num])[0]
        lexeme = test.lexeme
        for lex in lexeme:
            text = text.replace(f' {lex.word} ', f" {num}## ")

    dozens = {10: 'десятое', 20: 'двадцатое', 30: 'тридцатое', 40: 'сороковое', 50: 'пятидесятое',
              60: 'шестидесятое', 70: 'семидесятое', 80: 'восьмидесятое', 90: 'девяностое'}
    for num in dozens.keys():
        test = morph.parse(dozens[num])[0]
        lexeme = test.lexeme
        for lex in lexeme:
            text = text.replace(f' {lex.word} ', f" {num}## ")

    numbers = {1: 'первый', 2: 'второй', 3: 'третий', 4: 'четвертый', 5: 'пятый',
               6: 'шестой', 7: 'семой', 8: 'восьмой', 9: 'девятый', 0: 'нулевой'}
    for num in numbers.keys():
        test = morph.parse(numbers[num])[0]
        lexeme = test.lexeme
        for lex in lexeme:
            text = text.replace(f' {lex.word} ', f" {num}## ")

    numbers = {1: 'один', 2: 'два', 3: 'три', 4: 'четыре', 5: 'пять',
               6: 'шесть', 7: 'семь', 8: 'восемь', 9: 'девять', 0: 'ноль'}
    for num in numbers.keys():
        test = morph.parse(numbers[num])[0]
        lexeme = test.lexeme
        for lex in lexeme:
            text = text.replace(f' {lex.word} ', f" {num}## ")

    numbers = {11: 'одиннадцатого', 12: 'двенадцатого', 13: 'тринадцатого', 14: 'четырнадцатого', 15: 'пятнадцатого',
               16: 'шестнадцатого', 17: 'семнадцатого', 18: 'восемнадцатого', 19: 'девятнадцатого'}
    for num in numbers.keys():
        test = morph.parse(numbers[num])[0]
        lexeme = test.lexeme
        for lex in lexeme:
            text = text.replace(f' {lex.word} ', f" {num}## ")

    numbers = {11: 'одиннадцать', 12: 'двенадцать', 13: 'тринадцать', 14: 'четырнадцать', 15: 'пятнадцать',
               16: 'шестнадцать', 17: 'семнадцать', 18: 'восемнадцать', 19: 'девятнадцать'}
    for num in numbers.keys():
        test = morph.parse(numbers[num])[0]
        lexeme = test.lexeme
        for lex in lexeme:
            text = text.replace(f' {lex.word} ', f" {num}## ")

    text = re.sub("## ([0-9])", "##\\1", text)
    text = re.sub("([0-9]) ([0-9])", "\\1##\\2", text)

    text = text.replace(" го ", " ")

    text = re.sub("([0-9])##1000000", "\\1*1000000", text)
    text = re.sub("##([0-9]) ", "+\\1 ", text)

    text = re.sub("([0-9])##([0-9]{3})([^0-9])", "\\1+\\2\\3", text)
    text = re.sub("([0-9])##([0-9]{2})([^0-9])", "\\1+\\2\\3", text)
    text = re.sub("([0-9])##([0-9])([^0-9])", "\\1+\\2\\3", text)

    text = re.sub("[\\D+]([0-9]{3}[+][0-9]{2})##1000", "+(\\1)##1000", text)
    text = re.sub("##1000([^0-9])", "*1000\\1", text)

    text = re.sub("([0-9])## ", "\\1 ", text)
    text = re.sub("([0-9])##([0-9])", "\\1+\\2", text)

    pattern = re.compile(r'([0-9+)(*]+)')

    for (letters) in re.findall(pattern, text):
        letters = letters.lstrip('0')
        if len(letters) == 0:
            continue
        text = text.replace(f' {letters} ', f' {str(eval(letters))} ')

    return text.strip()


def anglicisms2russian(text: str):
    text = text.replace("visa", "виза")
    text = text.replace("mir", "мир")
    text = text.replace(" mир ", " мир ")
    text = text.replace("pay", "пей")
    text = text.replace("mobile", "мобайл")
    text = text.replace("online", "онлайн")
    text = text.replace("rsb", "рсб")
    text = text.replace("кэш бек", "кэшбек")
    text = text.replace("cashback", "кэшбек")
    text = text.replace("сashback", "кэшбек")
    text = text.replace("kari", "кари")
    text = text.replace("кэфси", "кфс")
    text = text.replace("kfc", "кфс")
    text = text.replace("teboil", "тебойл")
    text = text.replace("globus", "глобус")
    text = text.replace("vprok", "впрок")
    text = text.replace(" ru ", " ру ")
    text = text.replace(" c ", " с ")
    text = text.replace("sms", "смс")

    text = re.sub("master.?card|мастер.?кар[дт]", "мастер карт", text)
    text = re.sub("union.?pay|юнион.?пей", "юнионпей", text)
    text = re.sub("black.?friday|блэк.?фрайдей", "блэк фрайдей", text)
    text = re.sub("american.?express|американ.?эксперсс|amex", "американэксперсс", text)
    return text


def fix_misspell(text: str):
    print(f'before: {text}')
    text = f' {text} '
    spell = SpellChecker(language='ru')
    misspelled = spell.unknown(text.split(' '))
    for word in misspelled:
        if spell.correction(word):
            print(word)
            print(spell.correction(word))
            text = text.replace(f' {word} ', f' {spell.correction(word)} ')
    print(f'after: {text}')
    return text.strip()


def format_text(text: str):
    text = text.lower()
    text = text.replace("ё", "е")
    text = text.replace("%", " процент ")
    text = text.replace("процентов", "процент")
    pattern = re.compile(r'([0-9]+ ?[\\-] ?[0-9]+)')
    for (letters) in re.findall(pattern, text):
        letters = letters.lstrip('0')
        if len(letters) == 0:
            continue
        text = text.replace(f' {letters} ', f' {str(eval(letters.replace("-", "+")))} ')

    text = re.sub("[^0-9A-zА-яё]", " ", text)
    text = re.sub(" +", " ", text).strip()
    text = re.sub("([0-9]) ([0-9])", "\\1\\2", text)
    text = anglicisms2russian(text)
    text = word_number2number(text)
    # text = fix_misspell(text)
    return text


def main():
    whisper_model = whisper.load_model("tiny", device='cuda')
    # whisper_model = whisper.load_model("small", device='cuda')

    with open(json_file_path) as f:
        data = json.load(f)

    for rec in data:
        if os.path.isfile(f'{path_sound}{rec}.wav'):
            print(f'{path_sound}{rec}.wav')
            reference = format_text(data[rec]['TEXT'])
            transcribe = transcribe_file(f'{path_sound}{rec}.wav', whisper_model, "ru")
            hypothesis = format_text(transcribe)
            print(data[rec]['TEXT'])
            print(transcribe)
            print("###format:###")
            print(reference)
            print(hypothesis)

            error = wer(reference, hypothesis)
            result.append(error)
            print(f'{error}\n')
        else:
            print(f'WARNING no found file {path_sound}{rec}.wav')

    print('END')
    print(f'avg={round(sum(result) / len(result) * 100, 2)}')


# t = "семьсот один и два миллиона сто двадцать тысяч сто по двадцать первое января две тысячи двадцать первого года"
# print(word_number2number(t))
main()
