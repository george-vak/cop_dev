import calendar
import sys


def gen_calend(year, month):
    calend = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]

    rest = f".. table:: {month_name} {year}\n\n"
    rest += "    == == == == == == ==\n"
    rest += "    Mo Tu We Th Fr Sa Su\n"
    rest += "    == == == == == == ==\n"

    for week in calend:
        line = "    "
        for day in week:
            if day == 0:
                line += "   "
            else:
                line += f"{day:2d} "
        rest += line.rstrip() + "\n"

    rest += "    == == == == == == ==\n"
    return rest


if __name__ == "__main__":
    if len(sys.argv) != 3:
        exit(1)

    year = int(sys.argv[1])
    month = int(sys.argv[2])

    if month >= 1 or month <= 12:
        print(gen_calend(year, month))
