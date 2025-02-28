from ics import Calendar, Event
from openai import OpenAI
import datetime
import holidays
import calendar
import arrow
import json
import os


def generate_ics(date_list: list[tuple]) -> str:
    cal = Calendar()
    for i in date_list:
        event = Event()
        event.name = i[1]
        event.begin = arrow.get(i[0], "YYYY-MM-DD").replace(tzinfo="Asia/Seoul")
        event.end = arrow.get(i[0], "YYYY-MM-DD").replace(tzinfo="Asia/Seoul")
        event.make_all_day()
        cal.events.add(event)
    return str(cal)


def translate_to_japanese(data: list[str]) -> map:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": """\
以下の韓国語を日本語に翻訳してください。翻訳の際には以下のフォーマットに従ってください。

韓国語の意味を表記 (韓国語の読みをカタカナで表記／元の韓国語を表記)

例えば、以下のようになります。

旧正月(ソルナル／설날)

出力をそのまま利用したいので、改行区切りのテキストとして回答してください。データに適さない返答は不要です。
---
"""
                + "\n".join(data),
            }
        ],
        model="gpt-4o-mini",
    )
    translated = chat_completion.choices[0].message.content.split("\n")
    result = {}
    for i in range(len(translated)):
        result[data[i]] = translated[i].strip()
    return result


def main():
    kr_holidays = holidays.country_holidays("KR")
    base_dir = "dist/"

    date_list = []
    datetime_list = []
    holidays_names = set()
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
                        # Workaround for holiday name
                        if l == "신정연휴":
                            l = "신정"
                        holidays_names.add(l)
                        date_list.append(
                            {"date": current_date.strftime("%Y-%m-%d"), "ko": l}
                        )
                        datetime_list.append(
                            {
                                "datetime": int(current_date.timestamp()),
                                "ko": l,
                            }
                        )

    response = translate_to_japanese(list(holidays_names))
    for x in date_list:
        x.update({"ja": response[x["ko"]]})

    for x in datetime_list:
        x.update({"ja": response[x["ko"]]})

    os.makedirs(base_dir, exist_ok=True)

    # Generate ics file
    ics_ko = generate_ics([(x["date"], x["ko"]) for x in date_list])
    with open(base_dir + "ko.ics", "w") as outfile:
        outfile.write(ics_ko)

    ics_ja = generate_ics([(x["date"], x["ja"]) for x in date_list])
    with open(base_dir + "ja.ics", "w") as outfile:
        outfile.write(ics_ja)

    # Write json and csv files
    with open(base_dir + "date.json", "w") as outfile:
        json.dump(date_list, outfile, ensure_ascii=False, indent=2)

    with open(base_dir + "date.csv", "w") as outfile:
        for i in date_list:
            outfile.write(f"{i['date']},{i['ko']},{i['ja']}\n")

    with open(base_dir + "datetime.json", "w") as outfile:
        json.dump(datetime_list, outfile, ensure_ascii=False, indent=2)

    with open(base_dir + "datetime.csv", "w") as outfile:
        for i in datetime_list:
            outfile.write(f"{i['datetime']},{i['ko']},{i['ja']}\n")


if __name__ == "__main__":
    main()
