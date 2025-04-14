import gettext
import locale

translation = gettext.translation("LineCount", "po", fallback=True)
_, ngettext = translation.gettext, translation.ngettext
print(locale.getlocale())

while line := input():
    count = len(line.split())
    print(ngettext("Entered {} word", "Entered {} words", count).format(count))
