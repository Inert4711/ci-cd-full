# Full CI/CD Pipeline

Полноценный конвейер с интеграцией безопасности на ранних этапах и стратегией деплоя Blue-Green.

## Цель пайплайна

Создание безопасного конвейера, который:
- Автоматически блокирует деплой при обнаружении критических уязвимостей
- Интегрирует безопасность в каждый этап разработки
- Реализует стратегию Blue-Green деплоя с документированным откатом

## Структура пайплайна

```yaml
name: Full CI/CD Pipeline

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  test-matrix:       # ← Валидация бизнес-логики
  trivy-scan:        # ← Сканирование уязвимостей в зависимостях (блокирует деплой!)
  bandit-scan:       # ← Анализ небезопасных паттернов в коде
  build:             # ← Сборка только после прохождения всех проверок
  deploy-staging:    # ← Автоматический деплой в стейджинг
  deploy-production: # ← Ручное подтверждение + симуляция Blue-Green
```

## Ключевые особенности

1. Сканирование уязвимостей через Trivy

```yaml
- uses: aquasecurity/trivy-action@master
  with:
    scan-type: fs
    severity: HIGH,CRITICAL
    exit-code: '1'
    ignore-unfixed: true
```
При обнаружении уязвимостей, пайплайн останавливается с ошибкой.

2. Анализ кода через Bandit

```yaml
- run: |
    bandit -r . \
      --severity-level medium \
      --confidence-level high \
      -f json \
      --output bandit_report.json || true
```
Выявляет небезопасные паттерны, например, непроверенные входные данные.

3. Настройка ручного подтверждения

```yaml
deploy-production:
  environment:
    name: production
```
Триггер production требует ручного подтверждения деплоя в продакшен.

## Структура проекта
```
проект/
├── app.py
├── requirements.txt
├── tests/
│   └── test_app.py
└── .github/workflows/
    └── full-cicd.yml
```
