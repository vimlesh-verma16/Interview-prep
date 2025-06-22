class Pizza:
    def __init__(self, size, cheese=True, pepperoni=False, bacon=False):
        self.size = size
        self.cheese = cheese
        self.pepperoni = pepperoni
        self.bacon = bacon

    def __str__(self):
        toppings = []
        if self.cheese:
            toppings.append("cheese")
        if self.pepperoni:
            toppings.append("pepperoni")
        if self.bacon:
            toppings.append("bacon")
        return f"{self.size} Pizza with " + ", ".join(toppings)


# -------- Builder --------
class PizzaBuilder:
    def __init__(self, size):
        self.size = size
        self.cheese = True
        self.pepperoni = False
        self.bacon = False

    def add_pepperoni(self):
        self.pepperoni = True
        return self

    def add_bacon(self):
        self.bacon = True
        return self

    def no_cheese(self):
        self.cheese = False
        return self

    def build(self):
        return Pizza(self.size, self.cheese, self.pepperoni, self.bacon)


# -------- Usage --------
pizza = PizzaBuilder("Large").add_pepperoni().add_bacon().build()
print(pizza)  # Output: Large Pizza with cheese, pepperoni, bacon


# 🧱 Builder Pattern – Definition

# The Builder Pattern is a creational design pattern that lets you construct complex objects step-by-step, allowing you to create different representations of the object using the same construction process.
# It separates object construction from its representation, making the process more flexible and readable.

""""
✅ When to Use the Builder Pattern

Use the Builder Pattern when:

    🔢 Object has many optional parameters

        Especially when not all parameters are needed every time.

    🏗️ Object construction is complex or has multiple steps

        e.g., setting parts in a specific order, applying constraints.

    📦 Want to avoid telescoping constructors

        Too many constructor overloads with different combinations become messy.

    🧪 You want immutable objects

        Builder helps build the object first, then freeze it.

    🔄 You want to reuse the construction logic

        Especially useful for creating variants of the same object (e.g., a car with or without a sunroof).

❌ When to Avoid the Builder Pattern

Avoid it when:

    🧸 Object is simple with few parameters

        Regular constructor or dataclass is enough.

    ⚙️ No variations or optional configs are needed

        Builder adds unnecessary complexity and boilerplate.

    🧪 Python-specific: use @dataclass or **kwargs

        If you just need to build flexible objects in Python, these are more concise.

    📉 Performance-critical scenarios

        The overhead of extra methods/objects might not be worth it.

"""


class Computer:
    def __init__(self, cpu, ram, storage, gpu, os):
        self.cpu = cpu
        self.ram = ram
        self.storage = storage
        self.gpu = gpu
        self.os = os

    def __str__(self):
        return (
            f"Computer with {self.cpu} CPU, {self.ram} RAM, {self.storage} storage, "
            f"{self.gpu} GPU, running {self.os}"
        )


class ComputerBuilder:
    def __init__(self):
        self.cpu = "Intel i5"
        self.ram = "8GB"
        self.storage = "512GB SSD"
        self.gpu = "Integrated"
        self.os = "Windows 11"

    def set_cpu(self, cpu):
        self.cpu = cpu
        return self

    def set_ram(self, ram):
        self.ram = ram
        return self

    def set_storage(self, storage):
        self.storage = storage
        return self

    def set_gpu(self, gpu):
        self.gpu = gpu
        return self

    def set_os(self, os):
        self.os = os
        return self

    def build(self):
        return Computer(self.cpu, self.ram, self.storage, self.gpu, self.os)


# Usage
computer = (
    ComputerBuilder()
    .set_cpu("Intel i9")
    .set_ram("32GB")
    .set_gpu("NVIDIA RTX 4080")
    .set_os("Linux")
    .build()
)
print(computer)
