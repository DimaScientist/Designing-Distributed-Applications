# Лабораторная работа № 1:
# Тема: "Клиент-серверная архитектура" 
---

## Основные технологии:

* __Язык__: Python 3.6
* __Библиотеки__: numpy, matplotlib, PIL, socket

## Описание основных модулей программы

* *modules*:
  *  *client.py* - модуль для отправки исходного изображение;
  *  *interceptor.py* - модуль, который перехватывает и искажает изображение;
  *  *server.py* - модуль, который получает и очищает изображение.
*  *utils* - вспомогательные функции.
*  *main.py* - основной модуль для запуска сервера, перехватчика и клиента.
*  *config.py* - конфигурации для сокетных соединений.  


## Пример работы:

Исходное изображение:

![Исходное изображение](https://github.com/DimaScientist/Designing-Distributed-Applications/blob/main/Lab1/examples/client.png)

Изображение, получаемое сервером:

![Искаженное изображение](https://github.com/DimaScientist/Designing-Distributed-Applications/blob/main/Lab1/examples/noise_image.png)


Изображение, очищаемое сервером:

![Очищенное изображение](https://github.com/DimaScientist/Designing-Distributed-Applications/blob/main/Lab1/examples/clear_image.png)


## Оенка потери при передачи от клиента к серверу

Исходный размер файла:

![Исходный размер](https://github.com/DimaScientist/Designing-Distributed-Applications/blob/main/Lab1/examples/client_file_size.png)

Размер файла, очищенного на сервере:

![Размер файла на сервере](https://github.com/DimaScientist/Designing-Distributed-Applications/blob/main/Lab1/examples/server_file_size.png)


### Для запуска надо:

1. Установить зависимости из `requirements.txt`
2. Запустить main.py
