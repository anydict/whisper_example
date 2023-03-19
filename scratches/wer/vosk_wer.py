import asyncio
import wave
import websockets
import json
import re
import pymorphy2
import os.path
from jiwer import wer

path_sound = 'sounds/'
json_file_path = r'file_text.json'
result = []


def transcribe_file(name: str):
    async def run_test(uri):
        text = ""
        async with websockets.connect(uri) as websocket:
            wf = wave.open(name, "rb")
            await websocket.send('{ "config" : { "sample_rate" : %d } }' % (wf.getframerate()))
            buffer_size = 64000  # 0.4 seconds of audio, don't make it too small otherwise compute will be slow
            while True:
                data = wf.readframes(buffer_size)

                if len(data) == 0:
                    break

                await websocket.send(data)
                response = json.loads(await websocket.recv())
                text += response.get('text', '')

            await websocket.send('{"eof" : 1}')
            response = json.loads(await websocket.recv())
            text += response.get('text', '')
            return text

    try:
        return asyncio.run(run_test('ws://localhost:2700'))
    except RuntimeError:
        print(f'ERROR in file {name}')
        return 'Null'
    except Exception as e:
        print(f'ERROR file={name} e={e}')
        return 'Null'


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
    return text


def main():
    with open(json_file_path) as f:
        data = json.load(f)

    for rec in data:
        if os.path.isfile(f'{path_sound}{rec}.wav'):
            print(f'{path_sound}{rec}.wav')
            reference = format_text(data[rec]['TEXT'])
            hypothesis = format_text(transcribe_file(f'{path_sound}{rec}.wav'))
            print(reference)
            print(hypothesis)

            error = wer(reference, hypothesis)
            result.append(error)
            print(error)
        else:
            print(f'WARNING no found file {path_sound}{rec}.wav')

    print('END')
    print(f'avg={round(sum(result) / len(result) * 100, 2)}')


# t = "семьсот один и два миллиона сто двадцать тысяч сто по двадцать первое января две тысячи двадцать первого года"
# print(word_number2number(t))
main()
