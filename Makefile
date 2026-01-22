# This is a regular comment, that will not be displayed

## ----------------------------------------------------------------------
## This is a help comment. The purpose of this Makefile is to demonstrate
## a simple help mechanism that uses comments defined alongside the rules
## they describe without the need of additional help files or echoing of
## descriptions. Help comments are displayed in the order defined within
## the Makefile.
## ----------------------------------------------------------------------
.PHONY: tests

help:  ## Display this help screen
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

dependency:    ## Создать окружение и установить зависимости (uv, etc...)
	curl -LsSf https://astral.sh/uv/install.sh | sh
	uv self update
	uv venv .venv 
	uv sync --locked 

lint:     ## Прогнать линтеры
	uv run ruff check --no-fix .
	uv run ruff format --check .
	uv run mypy app/

format:   ## Отформатировать код
	uv run ruff check --fix .
	uv run ruff format .

check:   ## Полная проверка кода
	@make lint
	@make tests

run-api:  ## Запустить приложение
	uv run uvicorn app.presentation.api.main:app --reload --host 0.0.0.0 --port 8080

tests:   ## Запустить тесты
	uv run pytest tests/
