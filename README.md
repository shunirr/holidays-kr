# holidays-kr / 韓国の祝日

This is a script that generates holidays in South Korea, formatted in JSON, CSV, and iCalendar.

- API Doc: https://holidays-kr.s5r.jp/

Inspired by [Holidays JP API](https://holidays-jp.github.io/) project.

## Useful features

We provide a translated iCalendar file. Normally, holidays are provided as local-language calendars.

日本語訳された「韓国の祝日」の iCalendar ファイルを提供しています。

- https://holidays-kr.s5r.jp/ja.ics

## How to process

We use the `https://github.com/vacanza/holidays` library that provides holidays for many countries.

1. Get holidays from the [vacanza/holidays](https://github.com/vacanza/holidays) lib
2. Translate to Japanese by OpenAI API
3. Convert to JSON, CSV and iCalendar format
4. Deploy to Web
