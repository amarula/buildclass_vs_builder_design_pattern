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


# Base car class
class Car:
    def __init__(self, make, model):
        self.make = make
        self.model = model
        self.components = Components()

    def echo(self):
        print(f"Building {self.make} {self.model}", end='')
        self.components.echo()
        print()


# Class Builder class to assemble a car based on the options
class CarBuilder:
    def __init__(self, args):
        self.car = Car(args.make, args.model)
        self.args = args

    def build(self):
        self.car.components.add(Engine(self.args.Engine))
        self.car.components.add(Transmission(self.args.Transmission))

        if self.args.GPS:
            self.car.components.add(GPSNavigation())
        if self.args.Camera:
            self.car.components.add(Camera())
        if self.args.Sunroof:
            self.car.components.add(Sunroof())
        return self.car


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-make')
    parser.add_argument('-model')
    parser.add_argument('-Engine')
    parser.add_argument('-Transmission')
    parser.add_argument('-GPS', action='store_true')
    parser.add_argument('-Camera', action='store_true')
    parser.add_argument('-Sunroof', action='store_true')
    args = parser.parse_args()

    # Create a car
    car_builder = CarBuilder(args)
    car = car_builder.build()

    car.echo()
