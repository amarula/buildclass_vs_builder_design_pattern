import __init__
from dyndesign import buildclass, decoratewith, dynconfig, ClassConfig, LocalClassConfig
import argparse

# Base component classes
class Engine:
    def __init__(self, engine_type):
        self.engine_type = engine_type or "V6"

    def echo(self):
        print(f"\tEngine: {self.engine_type}")


class Transmission:
    def __init__(self, transmission_type):
        self.transmission_type = transmission_type or "Manual"

    def echo(self):
        print(f"\tTransmission: {self.transmission_type}")


class GPSNavigation:
    def echo(self):
        print(f"\tGPS Navigation")


class Camera:
    def echo(self):
        print(f"\tBackup camera")


class Sunroof:
    def echo(self):
        print("\tSunroof")


# Sub-component classes
class EngineV6(Engine):
    def __init__(self):
        super().__init__("V6")


class EngineV8(Engine):
    def __init__(self):
        super().__init__("V8")


class AutomaticTransmission(Transmission):
    def __init__(self):
        super().__init__("Automatic")


class ManualTransmission(Transmission):
    def __init__(self):
        super().__init__("Manual")


# Class to manage car components
class Components:
    def __init__(self):
        self.components = []

    def add(self, component):
        self.components.append(component)

    def echo(self):
        if self.components:
            print(" with components:")
            for component in self.components:
                component.echo()


# Mixin class for luxury option
class LuxuryMixin:
    def add_luxury_components(self, func, *args):
        func(self, *args)
        self.components.add(Sunroof())
        self.components.add(Camera())

    def echo_luxury(self, func):
        func(self)
        print("(Luxury Edition)")


# DynConfig Configurator class
class CarConfigurator:
    Engine = {
        "V6": ClassConfig(component_class=EngineV6),
        "V8": ClassConfig(component_class=EngineV8),
        dynconfig.SWITCH_DEFAULT: ClassConfig(component_class=EngineV6),
    }
    Transmission = {
        "Manual": ClassConfig(component_class=ManualTransmission),
        "Automatic": ClassConfig(component_class=AutomaticTransmission),
        dynconfig.SWITCH_DEFAULT: ClassConfig(component_class=ManualTransmission),
    }
    GPS = ClassConfig(component_class=GPSNavigation)
    Camera = ClassConfig(component_class=Camera)
    Sunroof = ClassConfig(component_class=Sunroof)

    Luxury = ClassConfig(inherit_from=LuxuryMixin)

    DYNDESIGN_LOCAL_CONFIG = LocalClassConfig(
        component_attr="components",
        init_args_from_option=True,
        structured_component_type=Components
    )

# Base car class
@dynconfig(CarConfigurator)
class Car:
    @decoratewith("add_luxury_components")
    def __init__(self, make, model):
        self.make = make
        self.model = model

    @decoratewith("echo_luxury")
    def echo(self):
        print(f"Building {self.make} {self.model}", end='')
        self.components.echo()
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-make')
    parser.add_argument('-model')
    parser.add_argument('-Engine')
    parser.add_argument('-Transmission')
    parser.add_argument('-GPS', action='store_true')
    parser.add_argument('-Camera', action='store_true')
    parser.add_argument('-Sunroof', action='store_true')
    parser.add_argument('-Luxury', action='store_true')
    args = parser.parse_args()

    # Create a car
    CarClass = buildclass(Car, args)
    car = CarClass(args.make, args.model)

    car.echo()
