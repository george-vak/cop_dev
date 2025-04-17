import gettext
import os
from functools import lru_cache

# Путь к папке локалей
localedir = os.path.join(os.path.dirname(__file__), "locale")

@lru_cache(maxsize=10)
def get_translator(locale: str) -> gettext.NullTranslations:
    try:
        return gettext.translation(
            domain="messages",
            localedir=localedir,
            languages=[locale],
            fallback=True
        )
    except Exception as e:
        print(f"[!] Ошибка загрузки переводов для {locale}: {e}")
        return gettext.NullTranslations()

def translate(text: str, locale: str = "en", **kwargs) -> str:
    translator = get_translator(locale)
    translated = translator.gettext(text)

    # Если строка без параметров — просто вернуть
    if not kwargs:
        return translated

    # Попробуем подставить параметры
    try:
        return translated.format(**kwargs)
    except Exception as e:
        print(f"[!] Ошибка форматирования строки: {translated} — {e}")
        return translated