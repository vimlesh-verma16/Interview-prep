from abc import ABC, abstractmethod


# -------- State Interface --------
class State(ABC):
    @abstractmethod
    def press_play(self, player):
        pass


# -------- Concrete States --------
class PlayingState(State):
    def press_play(self, player):
        print("Pausing the music...")
        player.state = PausedState()


class PausedState(State):
    def press_play(self, player):
        print("Resuming the music...")
        player.state = PlayingState()


# -------- Context --------
class MusicPlayer:
    def __init__(self):
        self.state = PausedState()  # Initial state

    def press_play(self):
        self.state.press_play(self)


# -------- Usage --------
player = MusicPlayer()
player.press_play()  # Output: Resuming the music...
player.press_play()  # Output: Pausing the music...
player.press_play()  # Output: Resuming the music...


print("\n\n\n\n\n")


# 🎯 What Is the State Pattern?

# The State Pattern allows an object to change its behavior based on its internal state — as if it changes its class at runtime. Instead of writing long if/else or switch-case blocks to handle state-specific logic, each state is encapsulated in its own class.

# ✅ When to Use the State Pattern
# Use the State Pattern when:
#     Object Behavior Depends on State
#         Example: A media player behaves differently in playing, paused, or stopped states.
#     Too Many if/else or switch-case Conditions
#         If logic based on states is cluttering your code and making it hard to maintain.
#     You Want to Add/Remove States Easily
#         Each state is its own class, so adding a new state means adding a new class without touching the rest.
#     State Transitions Are Frequent and Complex
#         Especially when transitions require side-effects (e.g., logging, events, etc.)
#     Open/Closed Principle Matters
#         Want to extend behavior without modifying existing code.


# ❌ When NOT to Use the State Pattern
# Avoid it when:
#     You Have Only One or Two Simple States
#         Overhead of extra classes isn't worth it.
#     State Behavior Is Unlikely to Change
#         If it’s static and unlikely to grow in complexity.
#     Performance or Memory Is Critical
#         Creating multiple state objects might be overkill for lightweight or memory-constrained applications.
#     Team Is Not Familiar With Design Patterns
#         Might lead to confusion or misapplication, increasing complexity instead of reducing it.

# Traffic signal Example

from abc import ABC, abstractmethod


class TrafficLightState(ABC):
    @abstractmethod
    def change(self, light):
        pass

    @abstractmethod
    def display(self):
        pass


class RedState(TrafficLightState):
    def change(self, light):
        print("Changing from RED to GREEN")
        light.state = GreenState()

    def display(self):
        print("RED light - STOP")


class GreenState(TrafficLightState):
    def change(self, light):
        print("Changing from GREEN to YELLOW")
        light.state = YellowState()

    def display(self):
        print("GREEN light - GO")


class YellowState(TrafficLightState):
    def change(self, light):
        print("Changing from YELLOW to RED")
        light.state = RedState()

    def display(self):
        print("YELLOW light - CAUTION")


class TrafficLight:
    def __init__(self):
        self.state = RedState()

    def change(self):
        self.state.change(self)

    def show(self):
        self.state.display()


# Usage
light = TrafficLight()
light.show()  # RED
light.change()

light.show()  # GREEN
light.change()

light.show()  # YELLOW
light.change()

light.show()  # Back to RED


# ---------------------------------

from abc import ABC, abstractmethod


# ---------- State Interface ----------
class State(ABC):
    @abstractmethod
    def insert_money(self, context, amount):
        pass

    @abstractmethod
    def select_item(self, context, item):
        pass

    @abstractmethod
    def dispense(self, context):
        pass


# ---------- Context ----------
class VendingMachineContext:
    def __init__(self):
        self.inventory = {"coffee": 2, "tea": 1, "soda": 0}
        self.balance = 0
        self.selected_item = None

        # Initial state
        self.state = IdleState()

    def set_state(self, state: State):
        self.state = state

    def insert_money(self, amount):
        self.state.insert_money(self, amount)

    def select_item(self, item):
        self.state.select_item(self, item)

    def dispense(self):
        self.state.dispense(self)

    def __str__(self):
        return f"{self.state } this is vending machine state context"


# ---------- Idle State ----------
class IdleState(State):
    def insert_money(self, context, amount):
        context.balance += amount
        print(f"[Idle] Money inserted: ₹{amount}")
        # print(context)
        context.set_state(HasMoneyState())
        # print(context)

    def select_item(self, context, item):
        print("[Idle] Please insert money first.")

    def dispense(self, context):
        print("[Idle] Cannot dispense. No money or item selected.")

    def __str__(self):
        return "ideal state"


# ---------- Has Money State ----------
class HasMoneyState(State):
    def insert_money(self, context, amount):
        context.balance += amount
        print(f"[HasMoney] Additional ₹{amount} inserted.")

    def select_item(self, context, item):
        if item not in context.inventory:
            print(f"[HasMoney] {item} is not available.")
            return

        if context.inventory[item] == 0:
            print(f"[HasMoney] {item} is out of stock.")
            context.set_state(OutOfStockState())
        else:
            context.selected_item = item
            print(f"[HasMoney] {item} selected.")
            context.set_state(DispensingState())

    def dispense(self, context):
        print("[HasMoney] Please select an item first.")

    def __str__(self):
        return "has money state"


# ---------- Dispensing State ----------
class DispensingState(State):
    prices = {"coffee": 10, "tea": 5, "soda": 15}

    def insert_money(self, context, amount):
        print("[Dispensing] Please wait. Dispensing in progress.")

    def select_item(self, context, item):
        print("[Dispensing] Already selected. Dispensing...")

    def dispense(self, context):
        item = context.selected_item
        price = self.prices.get(item, 0)

        if context.balance < price:
            print(f"[Dispensing] Not enough money. {item} costs ₹{price}.")
            context.set_state(HasMoneyState())
            return

        # Dispense item
        context.inventory[item] -= 1
        context.balance -= price
        print(f"[Dispensing] Dispensed: {item}. Remaining balance: ₹{context.balance}")

        # Reset state
        context.selected_item = None
        context.set_state(IdleState())


# ---------- OutOfStock State ----------
class OutOfStockState(State):
    def insert_money(self, context, amount):
        print("[OutOfStock] Item is out of stock. Returning ₹{amount}.")
        context.balance = 0
        context.set_state(IdleState())

    def select_item(self, context, item):
        print("[OutOfStock] Cannot select. Item unavailable.")
        context.set_state(IdleState())

    def dispense(self, context):
        print("[OutOfStock] Cannot dispense. Item unavailable.")
        context.set_state(IdleState())


print("\n\n\n\n")
machine = VendingMachineContext()

machine.select_item("tea")  # Should ask to insert money
machine.insert_money(10)  # ₹10 inserted
machine.select_item("soda")  # Out of stock
machine.select_item("tea")  # Tea selected
machine.dispense()  # Dispenses tea

machine.insert_money(5)  # ₹5 inserted
machine.select_item("coffee")  # Select coffee
machine.dispense()  # Not enough money
machine.insert_money(5)  # ₹5 more
machine.dispense()  # Dispenses coffee
