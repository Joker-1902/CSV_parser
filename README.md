# Обработчик CSV-файлов

Примеры запуска скрипта: 
``` bash 
python main.py --file my_data.csv
```

## - Поддерживатся агрегаци с расчетом суммы(sum), среднего (avg), минимального (min) и максимального (max) значения
Для выполнения аггрегаций:
``` bash 
python main.py --file my_data.csv --aggregate "price=avg"
``` 

Для выполнения фильтраций 
``` bash 
python main.py --file my_data.csv --where "rating>4.7"
``` 