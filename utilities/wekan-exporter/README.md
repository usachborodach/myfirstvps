# Wekan Prometheus Exporter

Экспортёр метрик [Wekan](https://github.com/wekan/wekan) для Prometheus.
Читает данные напрямую из MongoDB Wekan и отдаёт их в текстовом формате
Prometheus по HTTP на эндпоинте `/metrics`. Промежуточные файлы не используются —
данные собираются в момент скрейпа.

## Метрики

| Метрика | Тип | Описание |
|---|---|---|
| `wekan_cards{board_title, list_title, status}` | gauge | Количество карточек в списке доски. `status` — `active` (неархивированные) или `archive` |
| `wekan_exporter_up` | gauge | `1` — MongoDB доступна, `0` — при скрейпе произошла ошибка (в этом случае отдаются последние успешные значения) |

Пример вывода `/metrics`:

```text
wekan_exporter_up 1.0
wekan_cards{board_title="work",list_title="Новые",status="active"} 0.0
wekan_cards{board_title="work",list_title="Новые",status="archive"} 18.0
```

## Требования

- Python 3.8+
- Прямой доступ на чтение к MongoDB, в которой Wekan хранит данные (коллекции `lists`, `cards`)
- Зависимости из `requirements.txt`: `prometheus-client`, `pymongo`, `PyYAML`

Установка:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Конфигурация досок

Экспортируются только доски, перечисленные в `boards_data.yml`
(по умолчанию лежит рядом со скриптом). Файл перечитывается на лету,
если добавить новую доску — рестарт не нужен:

```yaml
- _id: 6nEeTCXHcdq3GaqoT
  title: work
- _id: eyZsGfRcPAysgBbB3
  title: home
```

`_id` доски можно взять из коллекции `boards` в MongoDB Wekan:

```bash
mongosh wekan --eval 'db.boards.find({}, {_id: 1, title: 1}).toArray()'
```

## Запуск

```bash
.venv/bin/python wekan-exporter.py
```

Экспортёр работает как долгоживущий сервис и слушает `0.0.0.0:9464/metrics`.

### Параметры командной строки и переменные окружения

| Аргумент | Переменная окружения | По умолчанию | Описание |
|---|---|---|---|
| `--port` | `WEKAN_EXPORTER_PORT` | `9464` | HTTP-порт с `/metrics` |
| `--mongo-uri` | `WEKAN_MONGO_URI` | `mongodb://localhost:27017` | Строка подключения к MongoDB |
| `--db` | `WEKAN_MONGO_DB` | `wekan` | Имя базы данных Wekan |
| `--boards-file` | `WEKAN_BOARDS_FILE` | `boards_data.yml` рядом со скриптом | Список экспортируемых досок |
| `--cache-ttl` | `WEKAN_EXPORTER_CACHE_TTL` | `10` | Сколько секунд переиспользовать результат запросов к MongoDB между скрейпами |

Пример:

```bash
WEKAN_MONGO_URI=mongodb://mongo:27017 .venv/bin/python wekan-exporter.py --port 9464
```

## Настройка Prometheus

```yaml
scrape_configs:
  - job_name: wekan
    static_configs:
      - targets: ['<host>:9464']
```

## Примеры запросов (PromQL)

```promql
# Всего активных карточек на доске
sum by (board_title) (wekan_cards{status="active"})

# Самая «большая» доска по числу карточек
topk(1, sum by (board_title) (wekan_cards))

# Алерт: экспортёр не может прочитать MongoDB
wekan_exporter_up == 0
```

## Устройство

- `WekanCollector` — кастомный collector для `prometheus_client`: при скрейпе
  получает списки каждой доски и считает активные/архивные карточки одним
  aggregation-запросом `$group` на доску (вместо двух `count_documents` на каждый список).
- Результат кэшируется на `--cache-ttl` секунд, чтобы частые скрейпы
  не нагружали MongoDB.
- При недоступной MongoDB `/metrics` всё равно отдаётся: с `wekan_exporter_up 0`
  и последними успешными значениями метрик.
