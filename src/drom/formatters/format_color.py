from googletrans import Translator

translator = Translator()
def translate(word):
    return translator.translate(word).text

def format_color(color): 
    translated_color = translate(color).upper()
    return translated_color if translated_color != 'THE BLACK' else 'BLACK'