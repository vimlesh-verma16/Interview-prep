"""
Proxy Design Pattern - This is structural design pattern.
"""

from abc import ABC, abstractmethod


class AbstractCmd(ABC):

    @abstractmethod
    def execute(self, command):
        pass


class RealCmd(AbstractCmd):

    def execute(self, command):
        print(f"{command} command executed.")


class ProxyCmd(AbstractCmd):

    def __init__(self, user):
        self.is_authorized = False
        if user == "admin":
            self.is_authorized = True
        self.executor = RealCmd()
        self.restricted_commands = ["rm", "mv"]

    def execute(self, command):
        if self.is_authorized:
            self.executor.execute(command)
        else:
            if any(
                [command.strip().startswith(cmd) for cmd in self.restricted_commands]
            ):
                raise Exception(
                    f"{command} command is not allowed for non-admin users."
                )
            else:
                self.executor.execute(command)


if __name__ == "__main__":
    admin_executor = ProxyCmd("admin")
    other_executor = ProxyCmd("other")
    try:
        admin_executor.execute("ls -la")
        admin_executor.execute("rm -rf /")
        print("\n")
        other_executor.execute("ls -la")
        other_executor.execute("rm -rf")
    except Exception as e:
        print(e)


"""
🧱 Proxy Pattern – Definition

The Proxy Pattern is a structural design pattern that provides a placeholder or surrogate for another object to control access, add behavior, or delay instantiation of that object.
    🔁 Think of a proxy as a middleman between a client and the real object.
    
✅ When to Use Proxy Pattern

    You want to control access (e.g., permissions, auth).

    You need lazy loading of heavy resources.

    You want to add caching, logging, or monitoring.

    You're working with remote objects (like APIs or services).

    You need mocking for testing external dependencies.

❌ When to Avoid Proxy Pattern

    The object is lightweight and always used immediately.

    There's no need for access control or extra logic.

    It adds unnecessary complexity in a small/simple system.

    You're overengineering for no clear benefit.
    
    
| Type             | Purpose                        | Common Use Case                          |
| ---------------- | ------------------------------ | ---------------------------------------- |
| Protection Proxy | Access control                 | Authorization, admin-only access         |
| Virtual Proxy    | Lazy initialization            | Delay loading images, reports            |
| Remote Proxy     | Remote object communication    | API clients, microservices               |
| Smart Proxy      | Extra behavior (logging, etc.) | Logging, caching, monitoring             |
| Mock Proxy       | Testing                        | Unit tests without hitting real services |


"""
