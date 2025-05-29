from openai import OpenAI
import datetime
import holidays
import calendar
import hashlib
import arrow
import json
import os

translate_dict = {
    "개천절": "開天節",
    "광복절": "光復節",
    "기독탄신일": "キリスト降誕日",
    "부처님오신날": "仏陀降誕日",
    "삼일절": "三一節",
    "설날": "旧正月",
    "신정": "新年",
    "어린이날": "こどもの日",
    "임시공휴일": "臨時休日",
    "지방선거일": "地方選挙日",
    "추석": "秋夕",
    "한글날": "ハングルの日",
    "현충일": "顕忠日",
    "국군의 날": "国軍の日",
    "국회의원 선거일": "国会議員選挙日",
    "대통령 선거일": "大統領選挙日",
    "설날 다음날": "旧正月 翌日",
    "설날 전날": "旧正月 前日",
    "추석 다음날": "秋夕 翌日",
    "추석 전날": "秋夕 前日",
    "개천절 대체 휴일": "開天節 代替休日",
    "광복절 대체 휴일": "光復節 代替休日",
    "부처님오신날 대체 휴일": "仏陀降誕日 代替休日",
    "삼일절 대체 휴일": "三一節 代替休日",
    "설날 대체 휴일": "旧正月 代替休日",
    "어린이날 대체 휴일": "こどもの日 代替休日",
    "추석 대체 휴일": "秋夕 代替休日",
}


def generate_ics(title: str, lang: str, date_list: list[tuple]) -> str:
    cal = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//github.com/shunirr/holidays-kr//{}".format(lang.upper()),
        "X-WR-CALNAME:{}".format(title),
        "X-WR-TIMEZONE:Asia/Tokyo",
        "X-WR-CALDESC:https://github.com/shunirr/holidays-kr",
    ]
    dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    for i in date_list:
        date = (
            arrow.get(i[0], "YYYY-MM-DD")
            .replace(tzinfo="Asia/Seoul")
            .format("YYYYMMDD")
        )
        uid = hashlib.sha1("{}-{}".format(date, i[1]).encode("utf-8")).hexdigest()
        cal.append("BEGIN:VEVENT")
        cal.append("DTSTART;VALUE=DATE:{}".format(date))
        cal.append("DTSTAMP:{}".format(dtstamp))
        cal.append("UID:{}".format(uid))
        cal.append("SUMMARY:{}".format(i[1]))
        cal.append("CLASS:PUBLIC")
        cal.append("TRANSP:TRANSPARENT")
        cal.append("END:VEVENT")
    cal.append("END:VCALENDAR")
    return "\n".join(cal)


def translate_to_japanese(data: list[str]) -> map:
    result = {}
    untranslated = []

    print("input:", data)

    # First, use translate_dict for known translations
    for item in data:
        if item in translate_dict:
            result[item] = f"{translate_dict[item]} ({item})"
        else:
            untranslated.append(item)

    print("translated by known list:", result)

    # If there are untranslated items, use OpenAI API
    if untranslated:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API key is not set")
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions="You are a helpful assistant that translates Korean holidays to Japanese.",
            input="""\
以下の韓国語を日本語に翻訳してください。翻訳の際には以下のフォーマットに従ってください。

{日本語での意味を表記} ({元の韓国語を表記})

例えば、以下のようになります。

旧正月 (설날)
仏誕祭 代替休日 (부처님 오신 날 대체휴일)
秋夕 二日目 (추석 이틀)

出力をそのまま利用したいので、改行区切りのテキストとして回答してください。データに適さない返答は不要です。
---
"""
            + "\n".join(untranslated),
        )
        translated = response.output_text.splitlines()

        print("translated by OpenAI:", translated)

        for i in range(len(untranslated)):
            if i < len(translated):
                result[untranslated[i]] = translated[i].strip()

    return result


def main():
    kr_holidays = holidays.country_holidays("KR", language="ko")
    base_dir = "dist/"

    date_list = []
    datetime_list = []
    holidays_names = set()
    now = datetime.date.today()
    for k in range(-2, 2):
        current_year = now.year + k
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

    try:
        response = translate_to_japanese(list(holidays_names))
        for x in date_list:
            x.update({"ja": response[x["ko"]]})
        for x in datetime_list:
            x.update({"ja": response[x["ko"]]})
    except ValueError as e:
        print(f"An error occurred: {e}")

    os.makedirs(base_dir, exist_ok=True)

    # Generate ics file
    ics_ko = generate_ics("공휴일", "KO", [(x["date"], x["ko"]) for x in date_list])
    with open(base_dir + "ko.ics", "w") as outfile:
        outfile.write(ics_ko)

    if "ja" in date_list[0]:
        ics_ja = generate_ics(
            "韓国の祝日", "JA", [(x["date"], x["ja"]) for x in date_list]
        )
        with open(base_dir + "ja.ics", "w") as outfile:
            outfile.write(ics_ja)

    # Write json and csv files
    with open(base_dir + "date.json", "w") as outfile:
        json.dump(date_list, outfile, ensure_ascii=False, indent=2)

    with open(base_dir + "date.csv", "w") as outfile:
        for i in date_list:
            if "ja" in i:
                outfile.write(f"{i['date']},{i['ko']},{i['ja']}\n")
            else:
                outfile.write(f"{i['date']},{i['ko']}\n")

    with open(base_dir + "datetime.json", "w") as outfile:
        json.dump(datetime_list, outfile, ensure_ascii=False, indent=2)

    with open(base_dir + "datetime.csv", "w") as outfile:
        for i in datetime_list:
            if "ja" in i:
                outfile.write(f"{i['datetime']},{i['ko']},{i['ja']}\n")
            else:
                outfile.write(f"{i['datetime']},{i['ko']}\n")


if __name__ == "__main__":
    main()
