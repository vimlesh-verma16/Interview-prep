from abc import ABC, abstractmethod


# Observer Interface
class Observer(ABC):
    @abstractmethod
    def update(self, title: str):
        pass


# Subject Interface
class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer):
        pass

    @abstractmethod
    def detach(self, observer: Observer):
        pass

    @abstractmethod
    def notify(self, title: str):
        pass


# Concrete Observer
class Subscriber(Observer):
    def __init__(self, name: str):
        self.name = name

    def update(self, title: str):
        print(f"{self.name} received new article: {title}")


# Concrete Subject
class Publisher(Subject):
    def __init__(self):
        self.subscribers = []

    def attach(self, observer: Observer):
        self.subscribers.append(observer)

    def detach(self, observer: Observer):
        self.subscribers.remove(observer)

    def notify(self, title: str):
        for subscriber in self.subscribers:
            subscriber.update(title)

    def publish(self, title: str):
        print(f"\nPublishing article: {title}")
        self.notify(title)


# Simulation
if __name__ == "__main__":
    pub = Publisher()
    a = Subscriber("Alice")
    b = Subscriber("Bob")

    pub.attach(a)
    pub.attach(b)

    pub.publish("Observer Pattern in Python")

    pub.detach(b)
    pub.publish("Python Tips & Tricks")


# ✅ When to Use the Observer Pattern
# | Scenario                                                | Example                                              |
# | ------------------------------------------------------- | ---------------------------------------------------- |
# | ✅ Multiple objects need to react to one object's change | UI elements reacting to data change (MVC pattern)    |
# | ✅ You want to decouple publisher and subscriber         | A button click notifying listeners                   |
# | ✅ Dynamic subscription/unsubscription is needed         | Newsletters, RSS feeds, chatroom join/leave          |
# | ✅ You want to implement event-driven architecture       | Realtime systems, logging systems, trading platforms |

# 🚫 When NOT to Use
# | Scenario                                 | Why It’s a Problem                                                        |
# | ---------------------------------------- | ------------------------------------------------------------------------- |
# | ❌ You don’t need real-time updates       | Adds unnecessary complexity                                               |
# | ❌ Tight performance constraints          | Frequent notifications can be expensive                                   |
# | ❌ Too many observers or frequent updates | Can lead to memory leaks or performance issues                            |
# | ❌ You need strong coupling or guarantees | Observer pattern is **loosely coupled**, not good for strict control flow |


# 🧠 Design Tip
#     Combine Observer Pattern with Strategy, Command, or Mediator for complex systems.
#     Use weak references (e.g., weakref.WeakSet) in Python to avoid memory leaks in long-running systems.
