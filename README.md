# holidays-kr / 韓国の祝日

This is a script that generates holidays in South Korea, formatted in JSON, CSV, and iCalendar.

- API Doc: https://holidays-kr.s5r.jp/

Inspired by [Holidays JP API](https://holidays-jp.github.io/) project.

## Useful features

We provide a translated iCalendar file. Normally, holidays are provided as local-language calendars.

日本語訳された「韓国の祝日」の iCalendar ファイルを提供しています。

- https://holidays-kr.s5r.jp/ja.ics

## Development

### Prerequisites

This project uses [uv](https://github.com/astral-sh/uv) for dependency management. Please install uv first:

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Setup

1. Clone the repository
2. Install dependencies using uv:

```bash
uv sync
```

### Running the application

To run the application:

```bash
uv run python app.py
```

Or use the build script which also generates API documentation:

```bash
./build.sh
```

## How to process

We use the `https://github.com/vacanza/holidays` library that provides holidays for many countries.

1. Get holidays from the [vacanza/holidays](https://github.com/vacanza/holidays) lib
2. Translate to Japanese by OpenAI API
3. Convert to JSON, CSV and iCalendar format
4. Deploy to Web
