import inventory
import storage
from datetime import datetime

MENU = """------------------------------
Учёт оборудования
1. - Показать оборудование
2. - Добавить оборудование
3. - Поиск оборудования
4. - Изменение оборудования
5. - Убрать оборудование
0. - Выход
------------------------------
Введите число для выбора варианта:.. """

# 1
items = inventory.get()
def show(items):
    if not items:
        print("Список пуст")
        return
    print(f"{'№':<4} | {'Тип':<10} | {'Наименование':<25} | {'Каб.':<7} | {'Состояние':<15} | {'Добавлено'}")
    print("-" * 92)
    for item in items:
        print(f"{item['id']:<4} | "
            f"{((str(item['type'][:9])+'..') if len(item['type']) > 10 else item['type']+' '):<11}| "
            f"{((str(item['name'][:24])+'..') if len(item['name']) > 25 else item['name']+' '):<26}| "
            f"{((str(item['room'][:6])+'..') if len(item['room']) > 7 else item['room']+' '):<8}| "
            f"{item['status']:<15} | "
            f"{item['created_at']}")
    print("-" * 92+"\n")
# 2
def add():
    tip = input("Тип: ")
    name = input("Наименование: ")
    room = input("Аудитория: ")
    status = input("Статус: ").lower()
    while True:
        if status in ['1','2','3']:
            status = ["исправно", "требует ремонта", "списано"][int(status)-1]
        if(tip=="0" or name=="0" or room=="0" or status=="0"):
            print("Завершаю...")
            break
        ok, text = inventory.add_item(
            {"id": (max([x["id"] for x in items]) + 1) if items else 1, 
            "type": tip,
            "name": name,
            "room": room,
            "status": status,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
        )
        if ok:
            print(text)
            break
        elif text == "Ошибка: неверное состояние (должно быть: исправно, требует ремонта, списано).":
            print(text)
            status = input("Статус: ")
            continue
        else:
            print(text)
            tip = input("Тип: ")
            name = input("Наименование: ")
            room = input("Аудитория: ")
            status = input("Статус: ")
# 3
def search():
    key = input("Поиск по какому ключу?.. ")
    request = input("Что ищем?.. ")
    while True:
        if key in ['1','2','3','4','5']:
            key = ["id", "type", "name", "room", "status"][int(key)-1]
        if(key=="0" or request=="0"):
            print("Завершаю...")
            break
        ok, text = inventory.search(key,request)
        if ok:
            show(text)
            break
        elif text=="Ошибка. Неверный ключ, попробуйте ещё раз (1:№, 2:Тип, 3:Наименование, 4:Кабинет, 5:Состояние)":
            print(text)
            key = input("Поиск по какому ключу?.. ")
        else:
            print(text)
            break
# 4
def change():
    id = input("№ который меняем... ")
    key = input("Что именно меняем?.. ")
    request = input("На что меняем... ")
    while True:
        if key in ['2','3','4','5']:
            key = ["type", "name", "room", "status"][int(key)-2]
        if(id=="0" or key=="0" or request=="0"):
            print("Завершаю...")
            break
        ok, text = inventory.change(id, key, request)
        if ok:
            print(text)
            break
        elif text=="Ошибка. Неверный ключ, попробуйте ещё раз (2:Тип, 3:Наименование, 4:Кабинет, 5:Состояние)":
            print(text)
            key = input("Изменяем какое поле?.. ")
        else:
            print(text)
            break
# 5
def remove():
    while True:
        id = input("№ который удаляем... ")
        if(id=="0"):
            print("Завершаю... ")
            break
        confirm = input(f"Удалить №{id}? (y/n)")
        if confirm=="y":
            ok, text = inventory.remove(id)
            print(text)
            if ok:
                break
        elif confirm=="n":
            continue
        else:
            print("Завершаю...")
            break
# Основной алгоритм собсна
def main():
    try:
        inventory.load()
    except storage.StorageError as e:
        print(f"Ошибка загрузки данных: {e}")
        return
    actions = {
    "1": lambda: show(inventory.get()),
    "2": add,
    "3": search,
    "4": change,
    "5": remove,
    }
    try:
        while True:
            choice = input(MENU).strip()
            print()
            if choice == "0":
                print("Выхожу...\n")
                break
            action = actions.get(choice)
            if action is None:
                print("Неверный пункт меню, попробуйте ещё раз\n")
                continue
            try:
                action()
            except storage.StorageError as e:
                print(f"Ошибка сохранения: {e}\n")
    except (KeyboardInterrupt, EOFError):
        print("\nВыхожу...")

# Запуск программы только если запускается именно этот файлик
if __name__ == "__main__":
    main()
