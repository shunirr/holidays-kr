# holidays-kr

This is a script that generates holidays in South Korea, formatted in JSON, CSV, and iCalendar.

- API Document: https://holidays-kr.s5r.jp/

## Useful features

We provide a translated iCalendar file. Normally, holidays are provided as local-language calendars. A translated calendar is useful.

- https://holidays-kr.s5r.jp/ja.ics

## How to process

We use the `https://github.com/vacanza/holidays` library that provides holidays for many countries.

1. Get holidays from holidays lib
2. Translate to Japanese by OpenAI API
3. Convert to JSON, CSV and iCalendar format
4. Deploy to Cloudflare Pages

And, we provide files translated to Japanese using the OpenAI API.
