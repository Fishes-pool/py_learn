"""
Demo: 电商订单系统
场景：Product 基类 + 子类 + Order 类，展示继承、@property、__str__、@classmethod、@dataclass。
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


# ---- 1. 基类（抽象产品）----
class Product:
    _total_count = 0                          # 类属性：所有产品总数

    def __init__(self, name: str, price: float, sku: str):
        self.name = name
        self._price = price                   # _: 约定内部属性，通过 @property 访问
        self.sku = sku
        Product._total_count += 1

    @property
    def price(self) -> float:                 # getter
        return self._price

    @price.setter
    def price(self, value: float):            # setter：带验证
        if value < 0:
            raise ValueError(f"价格不能为负数：{value}")
        self._price = value

    @classmethod
    def total_count(cls) -> int:              # 类方法
        return cls._total_count

    @classmethod
    def from_dict(cls, data: dict):           # 工厂方法
        return cls(data["name"], data["price"], data["sku"])

    @staticmethod
    def validate_sku(sku: str) -> bool:       # 静态方法：工具函数
        return sku.isalnum() and len(sku) >= 4

    def get_display_price(self) -> str:
        return f"¥{self._price:,.2f}"

    def __str__(self) -> str:
        return f"{self.name} ({self.sku}) - {self.get_display_price()}"

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name!r}, price={self._price}, sku={self.sku!r})"


# ---- 2. 子类：实体商品 ----
class PhysicalProduct(Product):

    def __init__(self, name: str, price: float, sku: str,
                 weight_kg: float, stock: int = 0):
        super().__init__(name, price, sku)    # 调用父类 __init__
        self.weight_kg = weight_kg
        self._stock = stock

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, value: int):
        if value < 0:
            raise ValueError("库存不能为负数")
        self._stock = value

    @property
    def shipping_fee(self) -> float:          # 计算属性（只读）
        if self.weight_kg <= 1:
            return 8.0
        return 8.0 + (self.weight_kg - 1) * 3.0

    def __str__(self) -> str:
        return f"[实体] {super().__str__()} 库存:{self._stock} 运费:¥{self.shipping_fee:.1f}"


# ---- 3. 子类：数字商品 ----
class DigitalProduct(Product):

    def __init__(self, name: str, price: float, sku: str,
                 download_url: str, license_type: str = "single"):
        super().__init__(name, price, sku)
        self._download_url = download_url
        self.license_type = license_type

    @property
    def download_url(self) -> str:            # 只读属性
        return self._download_url

    @property
    def shipping_fee(self) -> float:
        return 0.0                            # 数字商品免运费

    def __str__(self) -> str:
        return f"[数字] {super().__str__()} ({self.license_type}授权)"


# ---- 4. 订单行：用 @dataclass 减少样板代码 ----
@dataclass
class OrderItem:
    product: Product
    quantity: int
    unit_price: float = field(init=False)     # init=False: 不通过构造函数设置

    def __post_init__(self):
        self.unit_price = self.product.price  # 下单时锁定价格

    @property
    def subtotal(self) -> float:
        return self.unit_price * self.quantity

    def __str__(self) -> str:
        return f"{self.product.name} × {self.quantity} = ¥{self.subtotal:,.2f}"


# ---- 5. 订单类 ----
class Order:
    _order_sequence = 0

    def __init__(self, customer_name: str):
        Order._order_sequence += 1
        self.order_id = f"ORD-{Order._order_sequence:04d}"
        self.customer_name = customer_name
        self.created_at = datetime.now()
        self._items: list[OrderItem] = []
        self._status = "pending"

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, new_status: str):
        valid = {"pending", "paid", "shipped", "completed", "cancelled"}
        if new_status not in valid:
            raise ValueError(f"无效状态：{new_status}")
        self._status = new_status

    def add_item(self, product: Product, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("数量必须大于 0")
        # 同产品增加数量
        for item in self._items:
            if item.product.sku == product.sku:
                item.quantity += quantity
                return
        self._items.append(OrderItem(product=product, quantity=quantity))

    @property
    def subtotal(self) -> float:
        return sum(item.subtotal for item in self._items)

    @property
    def shipping_fee(self) -> float:
        return sum(
            getattr(item.product, "shipping_fee", 0) * item.quantity
            for item in self._items
        )

    @property
    def total(self) -> float:
        return self.subtotal + self.shipping_fee

    def __str__(self) -> str:
        lines = [
            f"订单 {self.order_id} | {self.customer_name} | {self.status}",
            f"时间: {self.created_at.strftime('%Y-%m-%d %H:%M')}",
            "-" * 45,
        ]
        for item in self._items:
            lines.append(f"  {item}")
        lines += [
            "-" * 45,
            f"  商品小计: ¥{self.subtotal:,.2f}",
            f"  运费:     ¥{self.shipping_fee:,.2f}",
            f"  总计:     ¥{self.total:,.2f}",
        ]
        return "\n".join(lines)


# ---- 主程序 ----
if __name__ == "__main__":
    # 直接创建产品（PhysicalProduct 有额外的必填参数，不适合用基类工厂方法）
    laptop = PhysicalProduct("MacBook Pro 14", 14999.0, "MBP14M3",
                             weight_kg=1.6, stock=50)

    mouse = PhysicalProduct("Magic Mouse", 599.0, "MGMOUSE", weight_kg=0.1, stock=200)
    software = DigitalProduct("Final Cut Pro", 2299.0, "FCPRO1",
                               "https://apps.apple.com/...", license_type="single")

    # @property 演示
    print("=== 产品信息 ===")
    print(laptop)
    print(mouse)
    print(software)
    print(f"运费：laptop={laptop.shipping_fee}元，software={software.shipping_fee}元")

    # 价格修改（通过 setter）
    mouse.price = 499.0
    print(f"\nMagic Mouse 价格更新：{mouse.get_display_price()}")

    # SKU 验证（静态方法）
    print(f"\nSKU 验证：'MBP14M3' -> {Product.validate_sku('MBP14M3')}")
    print(f"SKU 验证：'ab' -> {Product.validate_sku('ab')}")

    # 创建订单
    print("\n=== 订单系统 ===")
    order = Order("Alice")
    order.add_item(laptop, 1)
    order.add_item(mouse, 2)
    order.add_item(software, 1)
    order.add_item(mouse, 1)      # 重复添加同产品，数量累加

    order.status = "paid"

    print(order)

    # 类方法：查看总产品数
    print(f"\n创建产品总数：{Product.total_count()}")

    # isinstance / type 检查
    print(f"\n类型检查：")
    print(f"  laptop 是 Product？ {isinstance(laptop, Product)}")
    print(f"  laptop 是 DigitalProduct？ {isinstance(laptop, DigitalProduct)}")
    print(f"  software 是 DigitalProduct？ {isinstance(software, DigitalProduct)}")
