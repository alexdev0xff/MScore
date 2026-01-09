# Mcore Container Specification

Документация описывает формат контейнера для ядра **Mcore**.

Контейнер — это **папка** в директории `containers/`, содержащая конфигурацию, скрипт запуска и данные сервера.

---

## Структура контейнера

```text
containers/<container_name>/
├── container.yaml
├── start.sh
├── server.jar
└── eula.txt
```
## Пример контейнера 
```json
name: hitech 1.12.2 // название
type: minecraft // НЕ ТРОГАТЬ

startup:
  command: bash start.sh // путь к  запуску
  auto_start: false // автозапуск

java:
  bin: java           # или /usr/lib/jvm/java-17/bin/java
  xms: 1024M // мин джава
  xmx: 4096M // макс джава
  flags: // флаги майна
    - "-XX:+UseG1GC"
    - "-XX:MaxGCPauseMillis=200"

server:
  jar: server.jar // ядро
  args: // аргументы
    - nogui

resources:
  cpu: // ядра
    cores: 2

```

