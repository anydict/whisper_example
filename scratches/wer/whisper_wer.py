import whisper
import json
import re
import pymorphy2
from jiwer import wer

path_sound = 'sounds/'
json_file_path = r'file_text.json'
result = []


def transcribe_file(name: str, model, language: str):
    decode_options = dict(language=language, fp16=True)
    transcribe_options = dict(task="transcribe", **decode_options)
    transcription = model.transcribe(name, **transcribe_options)
    return transcription["text"]


def text_number_to_number(text: str):
    morph = pymorphy2.MorphAnalyzer()

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

    text = re.sub("## ([0-9])", "##\\1", text)

    text = re.sub("([0-9])##1000000", "\\1*1000000", text)
    text = re.sub("##([0-9]) ", "+\\1 ", text)

    text = re.sub("([0-9])##([0-9]{3})([^0-9])", "\\1+\\2\\3", text)
    text = re.sub("([0-9])##([0-9]{2})([^0-9])", "\\1+\\2\\3", text)
    text = re.sub("([0-9])##([0-9])([^0-9])", "\\1+\\2\\3", text)

    text = re.sub("[\\D+]([0-9]{3}[+][0-9]{2})([^0-9])", "+(\\1)\\2", text)
    text = re.sub("##1000([^0-9])", "*1000\\1", text)

    text = re.sub("([0-9])## ", "\\1 ", text)

    pattern = re.compile(r'([0-9+)(*]+)')

    for (letters) in re.findall(pattern, text):
        text = f' {text} '.replace(f' {letters} ', f' {str(eval(letters))} ')

    return text.strip()


def format_text(text: str):
    text = text.lower()
    text = text.replace("ё", "е")
    text = text.replace("%", " процент ")
    text = text.replace("процентов", "процент")
    text = re.sub("([0-9]+) +([0-9]+)", "\\1\\2", text)
    text = re.sub("([0-9]+) +([0-9]+)", "\\1\\2", text)
    text = text_number_to_number(text)
    text = re.sub("[^A-zА-я0-9 ]", " ", text)
    text = re.sub(" +", " ", text).strip()
    return text


def main():
    whisper_model = whisper.load_model("small", device='cuda')

    with open(json_file_path) as f:
        data = json.load(f)

    for rec in data:
        print(f'{path_sound}{rec}.wav')
        reference = format_text(data[rec]['TEXT'])
        hypothesis = format_text(transcribe_file(f'{path_sound}{rec}.wav', whisper_model, "ru"))
        print(reference)
        print(hypothesis)

        error = wer(reference, hypothesis)
        result.append(error)
        print(error)

    print('END')
    print(f'avg={round(sum(result) / len(result) * 100, 2)}')


# text = "восточный на два миллиона сто двадцать тысяч сто по двадцать первое января две тысячи двадцать первого года"
# print(text_number_to_number(text))
main()
