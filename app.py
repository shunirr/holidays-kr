from ics import Calendar, Event
import datetime
import holidays
import calendar
import arrow
import json
import os


def generate_ics(date_list) -> str:
    cal = Calendar()
    for i in date_list:
        event = Event()
        event.name = i["name"]
        event.begin = arrow.get(i["date"], "YYYY-MM-DD").replace(tzinfo="Asia/Seoul")
        event.end = arrow.get(i["date"], "YYYY-MM-DD").replace(tzinfo="Asia/Seoul")
        event.make_all_day()
        cal.events.add(event)
    return str(cal)


def main():
    kr_holidays = holidays.country_holidays("KR")
    base_dir = "dist/"

    date_list = []
    datetime_list = []
    now = datetime.date.today()
    for k in reversed(range(0, 3)):
        current_year = now.year - k
        for i in range(1, 13):
            last_day_of_month = calendar.monthrange(current_year, i)[1]
            for j in range(1, last_day_of_month + 1):
                current_date = datetime.datetime(current_year, i, j)
                holiday = kr_holidays.get(current_date)
                if holiday:
                    for l in holiday.split("; "):
                        date_list.append(
                            {"date": current_date.strftime("%Y-%m-%d"), "name": l}
                        )
                        datetime_list.append(
                            {
                                "datetime": int(current_date.timestamp()),
                                "name": l,
                            }
                        )

    os.makedirs(base_dir, exist_ok=True)

    # Generate ics file
    ics_data = generate_ics(date_list)
    with open(base_dir + "holidays.ics", "w") as outfile:
        outfile.write(ics_data)

    # Write json and csv files
    with open(base_dir + "date.json", "w") as outfile:
        json.dump(date_list, outfile, ensure_ascii=False, indent=2)

    with open(base_dir + "date.csv", "w") as outfile:
        for i in date_list:
            outfile.write(f"{i['date']},{i['name']}\n")

    with open(base_dir + "datetime.json", "w") as outfile:
        json.dump(datetime_list, outfile, ensure_ascii=False, indent=2)

    with open(base_dir + "datetime.csv", "w") as outfile:
        for i in datetime_list:
            outfile.write(f"{i['datetime']},{i['name']}\n")


if __name__ == "__main__":
    main()
