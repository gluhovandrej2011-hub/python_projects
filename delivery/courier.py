from decimal import Decimal
class Courier:
    name: str
    experience: int
    rating: float
    completed_orders: int
    balance: Decimal
    is_busy: bool
    def __init__(
            self, 
            name: str,
            experience: int,
            rating: float,
            completed_orders: int, 
            balance: Decimal, 
            is_busy: bool,):
            if len(name) == 0:
                raise ValueError("имя не может быть пустым")
            if experience < 0:
                raise ValueError("опыт работы не может быть отрицательным")
            if rating < 0 or rating > 5:
                raise ValueError("рейтинг бывает только от 0 до 5")
            if completed_orders < 0:
                raise ValueError("выполненные заказы не могут быть отрицательным числом")
            if balance < 0:
                raise ValueError("баланс не может быть отрицательным")
            self.name = name
            self.experience = experience
            self.rating = rating
            self.completed_orders = completed_orders
            self.balance = balance
            self.is_busy = is_busy
        
    def print_info(self) -> None:
        print(f"имя: {self.name}")
        print(f"опыт: {self.experience} месяцев")
        print(f"рейтинг: {self.rating}")
        print(f"сделанных заказов: {self.completed_orders}")
        print(f"баланс: {self.balance:.2f}")
        print(f"занят сейчас:{'да' if self.is_busy else 'нет'}")
    def deliver_order(self, distance: float) -> None:
        raise NotImplementedError("этот метод реализуется подклассами")
    def _calculate_salary_for_order(self, distance: float) -> float:
        raise NotImplementedError("этот метод реализуется подклассами")
    def finish_shift(self) -> None:
        self.is_busy = False
        print("сменя окончена")
        print(f"сделанных заказов: {self.completed_orders}")
        print(f"окончательный баланс: {self.balance:.2f}")

