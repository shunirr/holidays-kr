from ics import Calendar, Event
import datetime
import holidays
import calendar
import arrow
import json
import os


def main():
    kr_holidays = holidays.country_holidays("KR")
    base_dir = "dist/api/v1/"

    date_map = {}
    datetime_map = {}
    now = datetime.date.today()
    for k in reversed(range(0, 3)):
        current_year = now.year - k
        for i in range(1, 13):
            last_day_of_month = calendar.monthrange(current_year, i)[1]
            for j in range(1, last_day_of_month + 1):
                current_date = datetime.datetime(current_year, i, j)
                holiday = kr_holidays.get(current_date)
                if holiday:
                    date_map[current_date.strftime("%Y-%m-%d")] = holiday
                    datetime_map[str(int(current_date.timestamp()))] = holiday

    os.makedirs(base_dir, exist_ok=True)

    # Generate ics file
    cal = Calendar()
    for k, v in date_map.items():
        event = Event()
        event.name = v
        event.begin = arrow.get(k, "YYYY-MM-DD").replace(tzinfo="Asia/Seoul")
        event.end = arrow.get(k, "YYYY-MM-DD").replace(tzinfo="Asia/Seoul")
        event.make_all_day()
        cal.events.add(event)

    with open(base_dir + "holidays.ics", "w") as outfile:
        outfile.write(str(cal))

    # Write json and csv files
    with open(base_dir + "date.json", "w") as outfile:
        json.dump(date_map, outfile, ensure_ascii=False, indent=2)

    with open(base_dir + "date.csv", "w") as outfile:
        for k, v in date_map.items():
            outfile.write(f"{k},{v}\n")

    with open(base_dir + "datetime.json", "w") as outfile:
        json.dump(datetime_map, outfile, ensure_ascii=False, indent=2)

    with open(base_dir + "datetime.csv", "w") as outfile:
        for k, v in datetime_map.items():
            outfile.write(f"{k},{v}\n")


if __name__ == "__main__":
    main()
