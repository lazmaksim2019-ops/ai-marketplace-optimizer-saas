<p align="center">
  <img src="ai_optimizer_card.png" alt="AI Marketplace Optimizer" width="800"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white"/>
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white"/>
  <img src="https://img.shields.io/badge/Gemini-8E75B2?style=for-the-badge&logo=googlebard&logoColor=white"/>
  <img src="https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwind-css&logoColor=white"/>
</p>

---

# AI Marketplace Optimizer

### Мультимодальный ИИ-SaaS сервис для селлеров на маркетплейсах. SEO-генерация, анализ изображений, детекция триггеров инфографики. Интеграция с API Wildberries и Ozon.

**AI Marketplace Optimizer** — полнофункциональное fullstack SaaS-приложение для мультимодальной генерации и SEO-оптимизации карточек товаров под Wildberries и Ozon на базе Google Gemini.

> **Бизнес-ценность:** Сокращение времени на подготовку контента в **10+ раз** за счет использования мультимодального ИИ, который «видит» товар на фото и «пишет» продающий текст под алгоритмы конкретной площадки.

---

## Ключевые возможности

### Мультимодальный анализ (Vision + Text)
ИИ не просто генерирует текст — он анализирует визуальный контекст (фотографии товара) для формирования точного описания. Gemini получает сырые байты изображения, что исключает лишние сетевые задержки.

### Marketplace-Adaptive Prompts
Жесткое разделение промптов под требования Wildberries (до 60 симв. заголовок) и Ozon (формулы с использованием ключевых слов).

| Параметр | Wildberries | Ozon |
|----------|-------------|------|
| **Заголовок** | Строгий лимит до 60 символов, без спама, без дублирования | Богатое наименование до 200 символов по формуле Тип + Бренд + Особенности |
| **Описание** | Нативный LSI-копирайтинг до 3000 символов, вплетение поисковых синонимов | Конверсионный b2c-текст с упором на выгоды |
| **Философия** | Плотный художественный текст с ключами | Маркетинговые триггеры для покупателя |

### Детектор триггеров инфографики
Автоматическая рекомендация по добавлению преимуществ на фото товара, основанная на анализе визуальных паттернов. ИИ выделяет сильные стороны: *«100% натуральная шерсть»*, *«Влагозащита IPX4»*, *«Премиальное качество»* — и рекомендует вынести их на обложку.

### Enterprise-Ready Архитектура
- **Асинхронное взаимодействие** — FastAPI async endpoints
- **SOCKS5-прокси** — стабильный доступ к API в РФ
- **Pydantic v2-валидация** — строгий контроль схем, предотвращение галлюцинаций
- **Graceful error handling** — обработка rate limiting (429) с понятными сообщениями

### Дополнительно
- Копирование результатов в буфер обмена одной кнопкой
- Адаптивная вёрстка (Desktop / Mobile)
- Skeleton loader на время генерации
- CORS настроен для работы фронтенда с бэкендом

---

## Архитектура системы

```
┌─────────────┐     ┌──────────────┐     ┌──────────────────┐
│  Next.js UI │────>│  FastAPI     │────>│  Google Gemini   │
│  (Frontend) │<────│  Gateway     │<────│  Vision + Text   │
└─────────────┘     └──────────────┘     └──────────────────┘
                           │
                    ┌──────┴──────┐
                    │  Pydantic   │
                    │  Validation │
                    └─────────────┘
```

```
├── backend/                    # FastAPI + Gemini API
│   ├── main.py                 # Эндпоинты, логика, CORS
│   ├── config.py               # Настройки из .env (API key, proxy)
│   ├── schemas.py              # Pydantic-схемы запросов и ответов
│   └── requirements.txt        # Зависимости Python
│
├── frontend/                   # Next.js + TypeScript + Tailwind
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.tsx        # Главный экран
│   │   │   ├── ResultCard.tsx       # Виджет результата с копированием
│   │   │   ├── TriggerTags.tsx      # Теги триггеров инфографики
│   │   │   └── SkeletonLoader.tsx   # Скелетон-лоадер
│   │   ├── api.ts              # Клиент для запросов к бэкенду
│   │   ├── types.ts            # TypeScript-интерфейсы
│   │   └── App.tsx             # Точка входа
│   ├── vite.config.ts          # Vite + Tailwind + Proxy на бэкенд
│   └── package.json
│
├── .gitattributes
└── README.md
```

---

## Технологический стек

| Уровень | Технологии |
|---------|-----------|
| **Frontend** | Next.js 19, TypeScript, Tailwind CSS v4, Lucide React |
| **Backend** | Python 3.11+, FastAPI (Async), Pydantic v2, httpx |
| **AI** | Google Gemini 3.1 Flash Lite (мультимодальное ядро) |
| **Infrastructure** | SOCKS5 Proxy для стабильного доступа к API в РФ |

---

## Быстрый старт

```bash
# Клонирование
git clone https://github.com/lazmaksim2019-ops/ai-marketplace-optimizer-saas.git
cd ai-marketplace-optimizer-saas

# Бэкенд
cd backend
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # Linux/Mac
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

```bash
# Запуск бэкенда
uvicorn main:app --reload --port 8000

# Фронтенд (в новом терминале)
cd frontend
npm install
npm run dev
```

Фронтенд доступен на `http://localhost:5173`, прокси на бэкенд настроен автоматически.

---

## API

### `POST /api/analyze`
Принимает `multipart/form-data`:

| Поле | Тип | Обязательный | Описание |
|------|-----|:---:|---------|
| `description` | string | ✅ | Текущее описание товара |
| `marketplace` | string | ❌ | `"wb"` или `"ozon"` (по умолчанию `"wb"`) |
| `file` | file | ❌ | Изображение товара |
| `image_url` | string | ❌ | Ссылка на изображение |

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

## Roadmap

- [x] MVP: генерация SEO-текста + триггеры инфографики
- [x] Дифференциация стратегий Wildberries / Ozon
- [x] Обработка rate limiting (429)
- [ ] Rich-контент (генерация HTML-лендинга для Ozon)
- [ ] Генерация alt-тегов для изображений
- [ ] История запросов (база данных)
- [ ] Анализ конкурентов (парсинг топ-10 карточек)

---

## Лицензия

Proprietary / Closed Source. Все права защищены.

---

## Автор

**Александр Лазаренко** — Fullstack Developer (React + FastAPI + AI)

[![Telegram](https://img.shields.io/badge/Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/your_nickname)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/your-username)

---

> *«AI не заменит селлера. Но селлер, использующий AI, заменит того, кто им не пользуется.»*
