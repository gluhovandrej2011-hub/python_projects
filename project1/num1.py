from dataclasses import dataclass
@dataclass
class Computer:
    def __init__(this, pc_id, brand, cpu, gpu, ram, ssd, weight, price, stock):
        this.pc_id = int(pc_id)
        this.brand = str(brand)
        this.cpu = str(cpu)
        this.gpu = str(gpu)
        this.ram = int(ram)
        this.ssd = int(ssd)
        this.weight = int(weight)
        this.price = int(price)
        this.stock = int(stock)
def get_pc_price(item):
    return item.price

def get_pc_performance(item):
    return item.ram + item.ssd
class Store:
    def __init__(this):
        this.computers = []
    def add_new_pc(this, pc_id, brand, cpu, gpu, ram, ssd, weight, price, stock):
        for pc in this.computers:
            if pc.pc_id == pc_id:
                return False
        
        new_item = Computer(pc_id, brand, cpu, gpu, ram, ssd, weight, price, stock)
        this.computers.append(new_item)
        return True 
    def remove_by_id(this, target_id):
        found_pos = -1
        current_pos = 0
        for pc in this.computers:
            if pc.pc_id == target_id:
                found_pos = current_pos
                break
            current_pos = current_pos + 1
        
        if found_pos != -1:
            this.computers.pop(found_pos)
            return True
        return False 
    def remove_by_list_number(this, list_number):
        index_to_remove = list_number - 1
        if index_to_remove >= 0 and index_to_remove < len(this.computers):
            this.computers.pop(index_to_remove)
            return True
        return False
    def find_by_ram_and_price(this, limit_ram, limit_price):
        results = []
        for pc in this.computers:
                if pc.ram >= limit_ram: 
                    if pc.price <= limit_price: 
                       results.append(pc)
        return results
    def sort_pcs_by_price(this):
        this.computers.sort(key=get_pc_price)
    def sort_pcs_by_performance(this):
        this.computers.sort(key=get_pc_performance, reverse=True)
    def increase_ram_by_id(this, target_id, additional_ram):
        for pc in this.computers:
            if pc.pc_id == target_id:
                pc.ram = pc.ram + additional_ram
                return True
        return False
    def set_sale_by_id(this, target_id):
        for pc in this.computers:
            if pc.pc_id == target_id:
                pc.price = pc.price * 9 // 10
                print("РАСПРОДАЖА")
                return True
        return False
    def show_cheapest_and_expensive(this):
        if not this.computers:
            print("Нет компьютеров в магазине.")
            return
        cheapest_pc = this.computers[0]
        expensive_pc = this.computers[0]
        
        for pc in this.computers:
            if pc.price < cheapest_pc.price:
                cheapest_pc = pc
            if pc.price > expensive_pc.price:
                expensive_pc = pc
        
        print("Самый дешевый компьютер:")
        print("  ID:", cheapest_pc.pc_id, "| Бренд:", cheapest_pc.brand, "| Цена:", cheapest_pc.price)
        print("Самый дорогой компьютер:")
        print("  ID:", expensive_pc.pc_id, "| Бренд:", expensive_pc.brand, "| Цена:", expensive_pc.price)
    def search_video_card(this, name_to_find):
        results = []
        for pc in this.computers:
            if name_to_find in pc.gpu:
                results.append(pc)
        return results
    def print_all_items(this):
        number = 1
        for pc in this.computers:
            print(number, ") ID:", pc.pc_id, "| Бренд:", pc.brand, "| CPU:", pc.cpu, "| GPU:", pc.gpu, "| RAM:", pc.ram, "GB | SSD:", pc.ssd, "GB | Вес:", pc.weight, "г | Цена:", pc.price, "| На складе:", pc.stock, "шт.")
            number = number + 1
my_shop = Store()
my_shop.add_new_pc(101, "ASUS", "i7", "RTX 3060", 16, 512, 2000, 120000, 5)
my_shop.add_new_pc(102, "MSI", "i5", "RTX 3050", 8, 256, 1800, 85000, 3)
my_shop.add_new_pc(103, "HP", "i9", "RTX 4080", 32, 1024, 2500, 250000, 2)
print("Список всех ПК:")
my_shop.print_all_items()
print("\nСортировка по цене:")
my_shop.sort_pcs_by_price()
my_shop.print_all_items()
print("\n Поиск самых выгодных (RAM 16+, Цена до 150к):")
promo_list = my_shop.find_by_ram_and_price(16, 150000)
for p in promo_list:
    print(p.brand, p.price)
print("\n Анализ цен:")
my_shop.show_cheapest_and_expensive()