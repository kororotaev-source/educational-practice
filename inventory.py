inventory = [
    {
        "id": 1,
        "type": "ПК",
        "name": "Intel Core i5, 16GB RAM, RTX 4090",
        "room": "101",
        "status": "исправно",
        "created_at": "2026-03-24 12:44"
    },
    {
        "id": 2,
        "type": "Мониторчикзов",
        "name": "LG 24' IPS",
        "room": "101",
        "status": "исправно",
        "created_at": "2026-03-24 12:44"
    },
    {
        "id": 3,
        "type": "ПК",
        "name": "AMD Ryzen 5, 8GB RAM",
        "room": "102",
        "status": "требует ремонта",
        "created_at": "2026-03-24 12:44"
    },
    {
        "id": 4,
        "type": "Принтер",
        "name": "HP LaserJet P1102",
        "room": "Лаборантская",
        "status": "исправно",
        "created_at": "2026-03-24 12:44"
    },
    {
        "id": 5,
        "type": "Монитор",
        "name": "Samsung 22'",
        "room": "103",
        "status": "списано",
        "created_at": "2026-03-24 12:44"
    }
]


def get():
    return inventory

def id_check(id):
    inv = get()
    for x in range(len(inv)):
        if id == str(inv[x]["id"]):
            return True
    return False

def val_add_item(item, exist_items):
    for field in ["type", "name", "room", "status"]:
        if not str(item.get(field, "")).strip():
            return False, f"Ошибка: поле '{field}' не может быть пустым."
        if len(str(item.get(field, ""))) < 2:
            return False, f"Ошибка: значение {field} должно быть не менее 2 символов"
        
    if item["status"] not in ["исправно", "требует ремонта", "списано"]:
        return False, "Ошибка: неверное состояние (должно быть: исправно, требует ремонта, списано)."
        
    if id_check(id):
        return False, f"Ошибка: оборудование с номером {item['id']} уже существует."
    
    return True, "Успех, итем добавлен"

def add_item(item):
    exist_items = get()
    ok, text = val_add_item(item, exist_items)

    if ok:
        exist_items.append(item)
        return True, text
    return False, text

def search(type, request):
    types = {"id": "id", "type": "типа", "name": "названия", "room": "кабинета", "status": "статуса"}
    inv = get()
    finds = []
    if type not in ['id','type','name','room','status']:
        return False, "Ошибка. Неверный ключ, попробуйте ещё раз"
    if not type:
        return False, "Ошибка. Пустое поле, попробуйте ещё раз"
    for x in range(len(inv)):
        if request in str(inv[x][type]):
            finds.append(inv[x])
    if finds:
        return True, finds
    return False, f"Такого {types[type]} не существует"

def change(id, type, request):
    inv = get()
    er = 0
    if not id_check(id):
        return False, "Говно"
    if type not in ['id','type','name','room','status']:
        return False, 1
    if not type:
        return False, "Ошибка. Пустое поле, попробуйте ещё раз"
    item = inv[int(id)-1]
    item[type] = request
    return True, "Успешно изменено"

def remove(id):
    inv = get()
    if not id_check(id):
        return False, "Говно"
    inv.pop(int(id)-1)
    return True, 'Успешно удалено'