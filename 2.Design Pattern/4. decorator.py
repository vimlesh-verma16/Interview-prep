# function based decorator


def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__} with {args} {kwargs}")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} returned {result}")
        return result

    return wrapper


@log_decorator
def add(x, y):
    return x + y


add(5, 3)  # Logs input and output

print("\n\n\n\n")


# Base class
class Image:
    def display(self):
        raise NotImplementedError


# Concrete Image
class BasicImage(Image):
    def __init__(self, filename):
        self.filename = filename

    def display(self):
        return f"Displaying {self.filename}"


# Decorator Base
class ImageDecorator(Image):
    def __init__(self, image):
        self.image = image


# Concrete Decorators
class WatermarkDecorator(ImageDecorator):
    def display(self):
        return self.image.display() + " + Watermark"


class ResizeDecorator(ImageDecorator):
    def display(self):
        return self.image.display() + " + Resized"


class GrayscaleDecorator(ImageDecorator):
    def display(self):
        return self.image.display() + " + Grayscale"


# Usage
image = BasicImage("photo.jpg")
decorated = GrayscaleDecorator(ResizeDecorator(WatermarkDecorator(image)))
print(decorated.display())
# Output: Displaying photo.jpg + Watermark + Resized + Grayscale


print("\n\n\n\n\n")


class Account:
    def operation(self):
        raise NotImplementedError


class BankAccount(Account):
    def operation(self):
        return "Accessing account balance"


class AccountDecorator(Account):
    def __init__(self, account):
        self.account = account


class LoggingDecorator(AccountDecorator):
    def operation(self):
        print("[LOG] Accessing account")
        return self.account.operation()


class SecurityDecorator(AccountDecorator):
    def operation(self):
        print("[SECURITY] Checking user permissions")
        return self.account.operation()


# Usage
account = BankAccount()
decorated = LoggingDecorator(SecurityDecorator(account))
print(decorated.operation())


"""

🎨 Decorator Pattern – Definition

The Decorator Pattern is a structural design pattern that lets you add new behavior to an object dynamically at runtime without changing its structure.

    Think of it as wrapping an object to add functionality — like putting a gift in multiple layers of wrapping paper 🎁.

✅ When to Use the Decorator Pattern

Use it when:

    🔧 You want to add functionality dynamically at runtime

        Example: Add logging, compression, or encryption to data streams.

    🚫 You want to avoid subclassing explosion

        Instead of creating TextBox, TextBoxWithScroll, TextBoxWithBorder, etc.

    🔄 Behavioral combinations need to be flexible and reusable

        You can stack decorators in any order or combination.

    🧩 You want to follow Open/Closed Principle

        Add new features without modifying the original class.



❌ When to Avoid the Decorator Pattern

Avoid it when:

    📦 Object behavior is fixed and doesn't change

        No need for dynamic flexibility — use inheritance or simple composition.

    🧠 Too many nested decorators make the code hard to read

        Excessive wrapping leads to debugging nightmares.

    🪓 You need access to original class internals

        Decorators usually wrap public interfaces only.

    🧪 Unit testing becomes complex

        Mocking decorated behavior can be tricky if stacked too deeply.


| Use Case          | Description                                     |
| ----------------- | ----------------------------------------------- |
| UI Components     | Add scrollbars, borders, shadows to a component |
| Middleware        | Logging, auth, rate-limiting in Flask/Django    |
| File I/O          | Add compression/encryption to file streams      |
| Logging Decorator | Wrap methods with logging logic                 |
| Retry Mechanism   | Wrap function with automatic retries on failure |


✅ Benefits of Class-Based Decorators

    Add behavior dynamically

    Composable (stackable)

    Adheres to Open/Closed Principle

    Cleaner than subclassing when you have many combinations of behavior


"""
