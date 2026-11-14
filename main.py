import inventory
import storage

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

PROMPTS = {
    "type": "Тип",
    "name": "Наименование",
    "room": "Аудитория",
    "status": "Статус (1 - исправно, 2 - требует ремонта, 3 - списано)",
}
# 1
items = inventory.get()

def cancel():
    print("Завершаю...\n")

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
# нормализация для функсий
["исправно", "требует ремонта", "списано"]

def ask_field(field,prefix=""):
    """Спрашивает значение, пока оно не станет допустимым. '0' - отмена (вернёт None)."""
    while True:
        inputed = input(f"{prefix}{PROMPTS[field]}: ").strip()
        if inputed == "0":
            return None
        value = inventory.normalize(inputed, field)
        error = inventory.check_field(value, field)
        if not error:
            print(str(error) + " (0 - отмена)")
            continue
        return value
 
def ask_item(prompt):
    """Спрашивает номер, пока не найдётся такая запись. '0' - отмена."""
    while True:
        inputed = input(prompt).strip()
        if inputed == "0":
            return None
        item = inventory.find_by_id(inputed)
        if item is not None:
            return item
        print("Ошибка. Неверный ID, попробуйте ещё раз (0 - отмена)")
 
def ask_key(prompt, keys):
    """keys - словарь {'номер': 'поле'}. '0' - отмена."""
    while True:
        inputed = input(prompt).strip()
        if inputed == "0":
            return None
        if inputed in keys:
            return keys[inputed]
        print("Ошибка. Неверный ключ, попробуйте ещё раз (0 - отмена)")

def add():
    values = {}
    for field in inventory.FIELDS:
        value = ask_field(field)
        if value is None:
            return cancel()
        values[field] = value
    print(inventory.add_item(values) + "\n")
# 3
def search():
    keys = {"1": "id", "2": "type", "3": "name", "4": "room", "5": "status"}
    key = ask_key("Поиск по какому ключу?.. (1:№, 2:Тип, 3:Наименование, 4:Кабинет, 5:Состояние) ", keys)
    if key is None:
        return cancel()
    request = input("Что ищем?.. ").strip()
    if request == "0":
        return cancel()
    ok, result = inventory.search(key, request)
    if ok:
        show(result)
    else:
        print(result + "\n")
# 4
def change():
    item = ask_item("№ который меняем... ")
    if item is None:
        return cancel()
    keys = {"2": "type", "3": "name", "4": "room", "5": "status"}
    field = ask_key("Что именно меняем?.. (2:Тип, 3:Наименование, 4:Кабинет, 5:Состояние) ", keys)
    if field is None:
        return cancel()
    value = ask_field(field, prefix="Новое значение - ")
    if value is None:
        return cancel()
    print(inventory.change(item["id"], field, value) + "\n")

# 5
def remove():
    item = ask_item("№ который удаляем... ")
    if item is None:
        return cancel()
    confirm = input(f"Удалить №{item['id']} ({item['name']})? (y/n): ").strip().lower()
    if confirm == "y":
        print(inventory.remove(item["id"]) + "\n")
    else:
        print("Удаление отменено.\n")
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