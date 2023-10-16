## Traceroute
Нет зависимостей.
Python-task traceroute

#### Usage:
```
python main.py --host {host} --ttl {max_ttl} --timeout {max_timeout}
```

#### Output:
```
1: 10.121.1.13 (None)
2: 10.121.0.2 (None)
3: 80.87.100.2 (br2-4020.lo-1.netangels.ru)
4: 194.85.107.41 (ekaterinburg-ix.rosprint.net)
5: 195.151.233.105 (Ekaterinburg-GIN-PE01-lt-0-0-0-2.rosprint.net)
6: 195.151.234.228 (Umbrella-PE01-ae0-0.rosprint.net)
7: *
8: 195.151.33.1 (None)
9: *
10: *
11: *
12: 46.17.206.11 (None)
Достигнут конечный узел.
```

#### Фичи:
[x] Поддержка IPv4
[] Поддержка IPv6
[x] Работа через ICMP (custom SEQ)
[x] Вывод таблицы трассировки с временем ответа
[x] Посылать $N$ запросов
[x] Задание интервала между запросами
[x] Задания таймаута ожидания
[x] Задания максимального ttl
[x] Задание размера пакета
