import inventory
import storage

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

def main():
    menu = """-------------------------
Учёт оборудования
1. - Показать оборудование
2. - Добавить оборудование
3. - Поиск оборудования
4. - Изменение оборудования
5. - Убрать оборудование
0. - Выход
-------------------------
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
            continue
        elif(choice=="3"):
            continue
        elif(choice=="4"):
            continue
        elif(choice=="5"):
            continue
        else:
            print("Йоу так нельзя писать\n")

if __name__ == "__main__":
    main()
