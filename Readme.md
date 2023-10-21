## Traceroute
Python-task traceroute

#### Использование:
```
python main.py --host {host} --ttl {max_ttl} --timeout {max_timeout} --seq {seq} --size {size} -n {n} --ipv {ipv} 
```
Параметры:
* host - хост или ip адресс
* max_ttl - максимальный ttl
* max_timeout - таймаут запросов
* seq - кастомный SEQ - по умолчанию он увеличивается с 0 до n запросов
* n - количество пакетов для одного ttl
* ipv - версия ip 4 или 6


#### Вывод:
```
Traceroute to ya.ru (2a02:6b8::2:242). Send 3 packets for 60 bytes each
 1: 2a09:5302:ffff::1 (gw.firstbyte.ru) 9.013 ms 2a09:5302:ffff::1 (gw.firstbyte.ru) 18.583 ms 2a09:5302:ffff::1 (gw.firstbyte.ru) 6.460 ms
 2: 2a0b:6cc1:7::d (None) 0.993 ms 2a0b:6cc1:7::d (None) 0.863 ms 2a0b:6cc1:7::d (None) 0.995 ms
 3: 2a0b:6cc1:7::2:5 (None) 1.155 ms 2a0b:6cc1:7::2:5 (None) 0.976 ms 2a0b:6cc1:7::2:5 (None) 0.982 ms
 4: 2001:7f8:20:101::208:93 (dante.yndx.net) 1.693 ms 2001:7f8:20:101::208:93 (dante.yndx.net) 1.985 ms 2001:7f8:20:101::208:93 (dante.yndx.net) 2.321 ms
 5: * * *
 6: 2a02:6b8::2:242 (ya.ru) 3.991 ms 2a02:6b8::2:242 (ya.ru) 3.917 ms 2a02:6b8::2:242 (ya.ru) 3.848 ms
Достигнут конечный узел.
```

#### Фичи:
* [x] Поддержка IPv4
* [x] Поддержка IPv6
* [x] Работа через ICMP (custom SEQ)
* [x] Вывод таблицы трассировки с временем ответа
* [x] Посылать $N$ запросов
* [x] Задание интервала между запросами
* [x] Задания таймаута ожидания
* [x] Задания максимального ttl
* [x] Задание размера пакета
