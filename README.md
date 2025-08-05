# ITMO AI Programs Telegram Bot

This repository contains a Telegram bot implemented in Python that helps prospective master's students at ITMO University compare two programs—**Artificial Intelligence** and **AI Product**—by parsing their study plans, answering questions about courses, and recommending elective courses based on the user's background.

## Features

- **Automatic Plan Download & Parsing**: Fetches the PDF study plans directly from the official landing pages and parses course information including semester and type (mandatory vs elective).
- **Interactive Chat**: Guides the user through selecting a program, entering their background levels (math, programming, ML), asking course-related questions, and getting personalized elective recommendations.
- **Dockerized**: Ready-to-run with Docker Compose; supports ARM64 and x86_64.
- **Code Quality**: Integrated Black, Ruff, and Mypy checks, plus unit tests with pytest.
- **Command Interface**: Supports `/start`, `/help`, `/courses`, `/info`, `/recommend`, `/cancel`.

## Repository Structure

```
project-root/
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── mypy.ini
├── config.yaml
├── .env.example
├── .gitignore
├── src/
│   ├── bot.py
│   ├── handlers/
│   │   ├── start.py
│   │   ├── program.py
│   │   ├── background.py
│   │   ├── query.py
│   │   ├── recommendations.py
│   │   ├── help.py
│   │   ├── courses.py
│   │   ├── info.py
│   │   └── common.py
│   ├── parsers/
│   │   ├── downloader.py
│   │   ├── pdf_parser.py
│   │   └── html_parser.py
│   ├── models/
│   │   ├── course.py
│   │   └── recommendation.py
│   └── utils/
│       ├── helpers.py
│       └── logging_config.py
├── tests/
│   ├── test_pdf_parser.py
│   ├── test_html_parser.py
│   └── test_recommendation.py
└── data/
├── raw/
└── processed/
```

## Getting Started

### Prerequisites

- Docker & Docker Compose
- A Telegram Bot token (via @BotFather)

### Configuration

1. Copy `.env.example` to `.env` and fill in your bot token and desired DB path:
   ```ini
   BOT_TOKEN=your_token_here
   DB_PATH=/app/data/processed/courses.db

2.	Adjust any settings in config.yaml if needed.


### Running the Bot

### Build and start services
```bash
docker compose up --build -d
```

### View logs
```bash
docker compose logs -f itmo_telegram_bot
```

### Usage

- /start — Initialize the dialog and choose a program.
- /help — Display available commands.
- /courses — List all courses for the selected program.
- /info — Show program title and description.
- After selecting a program, enter three numbers for your background levels (e.g., “4 3 2”).
- Ask questions by typing part of a course name.
- Type Рекомендации to get personalized elective recommendations.
- /cancel — Cancel the current dialog.

### Development

#### Install dev dependencies inside container
make setup-dev

#### Format check with Black
make fmt

#### Lint with Ruff
make lint

#### Type check with Mypy
make typecheck

#### Run unit tests
make test

#### Run all checks
make all
