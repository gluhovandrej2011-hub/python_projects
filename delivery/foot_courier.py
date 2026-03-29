from decimal import Decimal
from courier import Courier
class Foot_Courier(Courier):
    max_distance: float
    speed: float
    
    def __init__(
        self, 
        name: str,
        experience: int,
        rating: float,
        completed_orders: int, 
        balance: Decimal, 
        is_busy: bool,
        max_distance: float,
        speed: float,
    ):
        super().__init__(name, experience, rating, completed_orders, balance, is_busy)

        if max_distance < 0:
            raise ValueError("максимальная дистанция должна быть положительной")
        if speed <= 0:
            raise ValueError("скорость должна быть положительной")
        self.max_distance = max_distance
        self.speed = speed

    def print_info(self) -> None:
        super().print_info()
        print(f"максимальная дистанция: {self.max_distance} км")
        print(f"скорость: {self.speed} км/ч")
    def _calculate_salary_for_order(self, distance: float) -> float:
        base_rate = 25.0
        fix_price = 120.0
        return base_rate * distance + fix_price
    def deliver_order(self, distance: float) -> None:
        if distance > self.max_distance:
            raise ValueError(f"не можем доставить заказ. дистанция {distance} км превышает максимальную {self.max_distance} км")
        
        self.completed_orders += 1
        salary = self._calculate_salary_for_order(distance)
        self.balance += Decimal(salary)
        print(f"заказ доставлен на {distance} км. получено {salary:.2f}")