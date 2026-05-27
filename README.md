
![Project Banner](https://img.shields.io/badge/Status-Ready%20for%20Production-success?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-8E75B2?style=for-the-badge&logo=googlebard&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwind-css&logoColor=white)

---

# 🚀 AI Marketplace Optimizer (SaaS MVP)

### Интеллектуальная мультимодальная система генерации и SEO-оптимизации карточек товаров для Wildberries и Ozon на базе Gemini

**AI Marketplace Optimizer** — полнофункциональное fullstack-приложение, которое анализирует изображение и текстовое описание товара, а затем генерирует SEO-оптимизированные карточки, адаптированные под требования конкретного маркетплейса. Сервис использует мультимодальные возможности Google Gemini для сквозного анализа визуала и текста в один проход.

---

## ✨ Ключевые возможности

### 🧠 Мультимодальный анализ (Vision + Text)
Сервис принимает на вход изображение товара (загрузка файла или URL) и текущие характеристики, анализируя визуал и текст одновременно. Gemini получает сырые байты изображения, что исключает лишние сетевые задержки.

### 🎯 Дифференцированные SEO-стратегии под каждый маркетплейс

| Параметр | Wildberries | Ozon |
|----------|-------------|------|
| **Заголовок** | Строгий лимит до 60 символов, без спама, без дублирования | Богатое наименование до 200 символов по формуле Тип + Бренд + Особенности |
| **Описание** | Нативный LSI-копирайтинг до 3000 символов, вплетение поисковых синонимов | Конверсионный b2c-текст с упором на выгоды (ранжирование Ozon зависит от характеристик, а не текста) |
| **Философия** | Плотный художественный текст с ключами | Маркетинговые триггеры для покупателя |

### 🏷️ Выделение триггеров для инфографики
ИИ автоматически вычленяет сильные стороны товара для выноса на обложку: «100% натуральная шерсть», «Влагозащита IPX4», «Премиальное качество» и т.д. Селлер может сразу перенести их в дизайн инфографики.

### 🛡️ Отказоустойчивость
Бэкенд корректно обрабатывает ошибку `429 Too Many Requests` (бесплатные ключи Google AI Studio имеют низкий приоритет). Пользователь вместо «белого экрана» видит понятное сообщение с инструкцией.

### 📋 Дополнительно
- Копирование результатов в буфер обмена одной кнопкой
- Адаптивная вёрстка (Desktop / Mobile)
- Skeleton loader на время генерации
- CORS настроен для работы фронтенда с бэкендом

---

## 🏗️ Архитектура

```
├── backend/                  # FastAPI + Gemini API
│   ├── main.py               # Эндпоинты, логика, CORS
│   ├── config.py             # Настройки из .env (API key, proxy)
│   ├── schemas.py            # Pydantic-схемы запросов и ответов
│   ├── requirements.txt      # Зависимости Python
│   └── .env                  # GEMINI_API_KEY и опционально PROXY
│
├── frontend/                 # React + Vite + TypeScript + Tailwind
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.tsx      # Главный экран
│   │   │   ├── ResultCard.tsx     # Виджет результата с копированием
│   │   │   ├── TriggerTags.tsx    # Теги триггеров инфографики
│   │   │   └── SkeletonLoader.tsx # Скелетон-лоадер
│   │   ├── api.ts            # Клиент для запросов к бэкенду
│   │   ├── types.ts          # TypeScript-интерфейсы
│   │   └── App.tsx           # Точка входа
│   ├── vite.config.ts        # Vite + Tailwind + Proxy на бэкенд
│   └── package.json
│
└── README.md
```

---

## 🛠️ Стек технологий

### Frontend
- **React 19** + **TypeScript** — типизированный UI
- **Vite** — быстрая сборка и HMR
- **Tailwind CSS v4** — утилитарная стилизация
- **Lucide React** — современные иконки

### Backend
- **Python 3.11+** + **FastAPI** — асинхронный REST API
- **Google GenAI SDK** (`google-genai`) — мультимодальный Gemini
- **Pydantic v2** — валидация данных
- **httpx** — HTTP-клиент (в т.ч. SOCKS5-прокси)

### AI
- **Gemini 3.1 Flash Lite** — быстрая мультимодальная модель
- Формат ответа: `response_mime_type="application/json"`

---

## 🚦 Быстрый старт

### 1. Клонирование
```bash
git clone https://github.com/your-username/ai-marketplace-optimizer.git
cd ai-marketplace-optimizer
```

### 2. Бэкенд
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # или .venv\Scripts\activate на Windows
pip install -r requirements.txt
```

Создайте `.env` в папке `backend`:
```env
GEMINI_API_KEY=ваш_ключ_google_ai_studio
# Опционально — SOCKS5-прокси для регионов без прямого доступа:
PROXY_HOST=your_proxy_host
PROXY_PORT=your_proxy_port
PROXY_USER=your_proxy_user
PROXY_PASS=your_proxy_pass
```

Запуск:
```bash
python -m uvicorn main:app --reload --port 8000
```

### 3. Фронтенд
```bash
cd frontend
npm install
npm run dev
```

Фронтенд доступен на `http://localhost:5173`, прокси на бэкенд настроен автоматически через `vite.config.ts`.

---

## 📡 API

### `POST /api/analyze`
Принимает `multipart/form-data`:
| Поле | Тип | Обязательный | Описание |
|------|-----|:---:|---------|
| `description` | string | ✅ | Текущее описание товара |
| `marketplace` | string | ❌ | `"wb"` или `"ozon"` (по умолчанию `"wb"`) |
| `file` | file | ❌ | Изображение товара |
| `image_url` | string | ❌ | Ссылка на изображение (альтернатива file) |

**Ответ:**
```json
{
  "seo_title": "Свитер мужской из натуральной шерсти",
  "seo_description": "Мужской свитер...",
  "infographics_triggers": ["100% натуральная шерсть", "Премиальное качество"],
  "marketing_tips": "Рекомендуем заменить фон на студийное фото"
}
```

### `GET /api/health`
Проверка работоспособности сервера.

---

## 📈 Roadmap

- [x] MVP: генерация SEO-текста + триггеры инфографики
- [x] Дифференциация стратегий Wildberries / Ozon
- [x] Обработка rate limiting (429)
- [ ] Rich-контент (генерация HTML-лендинга для Ozon)
- [ ] Генерация alt-тегов для изображений
- [ ] История запросов (база данных)
- [ ] Анализ конкурентов (парсинг топ-10 карточек)

---

## 🤝 Вклад в проект

Pull Request'ы приветствуются. Для крупных изменений, пожалуйста, откройте issue для обсуждения.

---

## 📄 Лицензия

MIT

---

## 👨‍💻 Автор

**Александр Лазаренко** — проект Fullstack Developer (React + FastAPI + AI)

[![Telegram](https://img.shields.io/badge/Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/your_nickname)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/your-username)

---

> ⚡ *«AI не заменит селлера. Но селлер, использующий AI, заменит того, кто им не пользуется.»*
