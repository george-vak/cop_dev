import gettext
import os
import re
from functools import lru_cache

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

    # Автообработка плуралов вида {points_something}
    plural_matches = re.findall(r"{points_(\w+)}", translated)
    for var_name in plural_matches:
        try:
            count = int(kwargs.get(var_name, 0))
            plural_form = translator.ngettext("point", "points", count)
            kwargs[f"points_{var_name}"] = plural_form
        except Exception as e:
            print(f"[!] Ошибка обработки множественного числа: {var_name} — {e}")

    try:
        return translated.format(**kwargs)
    except Exception as e:
        print(f"[!] Ошибка форматирования строки: {translated} — {e}")
        return translated