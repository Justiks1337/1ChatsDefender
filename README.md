# 1ChatsDefender
The defender of 1C chats

## Архитектура

Проект состоит из основного приложения и отдельного микросервиса для OCR (оптического распознавания символов):

- Основное приложение: Telegram бот для защиты чатов
- OCR микросервис: Отдельный сервис для извлечения текста из изображений

Детальная документация по OCR сервису доступна в [docs/ocr-service.md](docs/ocr-service.md).

## Микросервисы

### OCR Service

Микросервис для извлечения текста из изображений расположен в директории `ocr-service`.
Он предоставляет REST API для распознавания текста на изображениях с помощью EasyOCR.

Для работы основного приложения необходимо запустить OCR сервис:

```bash
cd ocr-service
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

Или через Docker:

```bash
cd ocr-service
docker build -t ocr-service .
docker run -p 8000:8000 ocr-service
```
