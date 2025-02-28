# holidays-kr

This is a script that generates holidays in South Korea, formatted in JSON, CSV, and iCalendar.

- https://holidays-kr.s5r.jp/

## How to process

We use the `https://github.com/vacanza/holidays` library that provides holidays for many countries.

1. Get holidays from holidays lib
2. Convert to JSON, CSV and iCalendar format
3. Deploy to Cloudflare Pages

And, we provide files translated to Japanese using the OpenAI API.
