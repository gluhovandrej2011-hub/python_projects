from decimal import Decimal
from foot_courier import Foot_Courier
foot_courier = None
try:
    foot_courier: Foot_Courier = Foot_Courier(
        name="Boris",
        experience=5,
        rating=4.3,
        completed_orders=99, 
        balance=Decimal("1234.00"), 
        is_busy=False,
        max_distance=8.0,
        speed=4.5,
    )
except ValueError as e:
    print(f"ошибка в создании курьера: {e}")
else:
    foot_courier.print_info()
    foot_courier.deliver_order(distance=5.0)
    foot_courier.finish_shift()
    foot_courier.print_info()