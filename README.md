# Импорт пользователей чатов Telegram

Экспортирует пользователей одного или нескольких чатов Telegram и импортирует в другой чат.


## Требования

* Python 3.x
* [Telethon library](https://github.com/LonamiWebs/Telethon)

## Подготовка

1. Устанавливаем зависимости:
   ```
   pip3 install -r requirements.txt
   ```

2. Заходим на [my.telegram.org](https://my.telegram.org), авторизуемся и получаем: 
   * API ID
   * API Hash

3. Переименовываем пример конфига [`config.example.py`](config.example.py) в `config.py` и меняем значения параметров на полученные в п. 2:

   * api_id
   * api_hash

4. Указываем список чатов (без `@`), откуда надо парсить пользователей:
   ```python
   export_chats = [ 
       'chat1_name',
       'chat2_name'
   ]
   ```

5. Указываем имя целевого чата (без `@`), куда будут импортированы пользователи:
   ```python
   target_chat = 'my_chat_name'
   ```

## Дополнительные параметры

* **Лимит импорта** — максимальное кол-во пользователей, которые будут импортированы (выбираются случайным способом), по умолчанию лимита нет (будут импортированы все):
  ```python
  import_limit = 10
  ```

* **Исключить админов** — при импорте пользователей по умолчанию администраторы чатов будут исключены:
  ```python
  exclude_admins = True
  ```

* **Исключить ботов** — при импорте пользователей по умолчанию боты будут исключены:
  ```python
  exclude_bots = True
  ```

* **Исключить удаленные аккаунты** — после удаления пользователя Telegram удаляет их полностью не сразу, некоторое время аккаунты еще числятся удаленными (помечаются как "Deleted account"), при импорте пользователей такие аккаунты по умолчанию не будут импортированы:
  ```python
  exclude_deleted = True
  ```

* **Исключить давно неиспользуемые аккаунты** — пользователи, которые не были онлайн указанное кол-во дней или дольше, будут исключены из импорта. По умолчанию: 30 дней. Для того, чтобы импортировать только пользователей, которые были онлайн недавно (Recently), укажите = 0.
  ```python
  exclude_offline_days = 30
  ```

* **Черный список** — список пользователей (без `@`), которых надо исключить из импорта в любом случае:
  ```python
  usernames_blacklist = [
      'username_1',
      'username_2'
  ]
  ```

## Логирование

Используется стандартная библиотека [`logging`](https://docs.python.org/3/library/logging.html).

### Уровень подробности

Для того, чтобы изменить уровень подробности логирования, поменяйте значение параметра (повлияет как на вывод в консоль, так и на файл лога):
```python
log_level = 'INFO'  # DEBUG | INFO | WARNING | ERROR | CRITICAL
```

### Вывод в консоль

Нельзя отключить, будет всегда.

### Логирование в файл — путь к логу

Укажите `'.'` — логирование будет в директории скрипта. Можно оставить пустым — логирования в файл не будет.
```python
log_path = ''  # log_path = '.' или log_path = '/tmp'
```

### Логирование в файл — имя файла

Оставьте пустым — файл лога будет `tg-chats-users-import.log` (формируется по шаблону `<имя_скрипта>.log`). Можно указать кастомное имя файла лога, оно будет дополнено суффиксом `.log`.
```python
log_name = ''  # log_name = 'my_log_name' -> my_log_name.log
```