import inventory
import storage
# 1
def show():
    items = inventory.get()
    print(f"{'№':<4} | {'Тип':<10} | {'Наименование':<25} | {'Каб.':<12} | {'Состояние'}")
    print("-" * 80)
    
    for item in items:
        print(f"{item['id']:<4} | "
              f"{item['type']:<10} | "
              f"{item['name']:<25} | "
              f"{item['room']:<12} | "
              f"{item['status']}")
    print("-" * 80+"\n")
# 2
def add():
    print("Будет добавление здесь короче")
# 3
def search():
    print("Будет поиск здесь короче")
# 4
def change():
    print("Будет изменение здесь короче")
# 5
def remove():
    print("Здесь удаление будет короче")
# Основной алгоритм собсна
def main():
    menu = """------------------------------
Учёт оборудования
1. - Показать оборудование
2. - Добавить оборудование
3. - Поиск оборудования
4. - Изменение оборудования
5. - Убрать оборудование
0. - Выход
------------------------------
Введите число для выбора варианта:.. """
    
    while True:
        choice = input(menu)
        print()
        if(choice=="0"):
            print("Выхожу...\n")
            break
        elif(choice=="1"):
            show()
        elif(choice=="2"):
            add()
        elif(choice=="3"):
            search()
        elif(choice=="4"):
            change()
        elif(choice=="5"):
            remove()
        else:
            print("Йоу так нельзя писать, давай заново\n")
# Запуск программы только если запускается именно этот файлик
if __name__ == "__main__":
    main()
