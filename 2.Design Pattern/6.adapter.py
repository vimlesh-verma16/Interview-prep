# Class with incompatible interface
class EuropeanSocket:
    def get_voltage(self):
        return 220


# Target interface
class AmericanAppliance:
    def plug_in(self, voltage):
        if voltage == 110:
            print("Appliance running safely on 110V.")
        else:
            print("⚠️ Voltage mismatch! Appliance might be damaged.")


# Adapter that converts 220V to 110V
class SocketAdapter:
    def __init__(self, european_socket):
        self.european_socket = european_socket

    def get_converted_voltage(self):
        original_voltage = self.european_socket.get_voltage()
        print(f"Adapter converting {original_voltage}V to 110V.")
        return 110  # Simulate conversion


# Client code
euro_socket = EuropeanSocket()
adapter = SocketAdapter(euro_socket)

appliance = AmericanAppliance()
appliance.plug_in(adapter.get_converted_voltage())


""" 
Definition:
    The Adapter Pattern allows incompatible interfaces to work together by acting as a bridge between them.
It’s like a translator or a power plug adapter — converting one interface into another expected one without changing existing code.


✅ When to Use Adapter Pattern
Use it when:
    ✅ You want to use a class, but its interface does not match what you need.
    ✅ You don’t want to (or can’t) modify the existing code.
    ✅ You want to make legacy code work with new code.
    ✅ You need to bridge two systems (e.g., old API vs new interface).

    
❌ When NOT to Use
Avoid it when:
    ❌ You can modify the existing class directly — no need for an adapter.
    ❌ Too many adapters clutter your code — consider refactoring.
    ❌ You’re using it as a shortcut instead of designing better interfaces.   
    
    
🧠 Adapter Pattern Types
Type	Description
Object Adapter	Uses composition – adapter holds a reference to the adaptee.
Class Adapter	Uses inheritance – adapter extends the adaptee class (less common in Python).

👎 Cons of Adapter Pattern
Limitation	Description
❌ Added Complexity	Adds an extra layer of abstraction.
❌ Overuse	Too many adapters = messy architecture.
❌ Not Always Efficient	If conversion logic is heavy, it could affect performance.


class OldSystem:
    def old_method(self):
        return "Old system working."

class NewSystemInterface:
    def new_method(self):
        pass

class Adapter(NewSystemInterface):
    def __init__(self, old_system):
        self.old_system = old_system

    def new_method(self):
        return self.old_system.old_method()

🔚 Summary
    🧰 Use it to adapt mismatched interfaces.
    🔌 Think of it as a plug converter.
    ✅ Great for reusing legacy or 3rd-party code.
    ❌ Don’t use it to hide bad design — prefer interface consistency when possible.
"""
