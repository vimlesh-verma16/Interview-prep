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
