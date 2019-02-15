"""
This script creates all possibilities of airplanes that guests can build in
the exhibit AR.02.08 Design a Plane, and then simulates if they can takeoff.
"""

import numpy as np
import pandas as pd

"""
The class Material sets the density of a material, so it can later be used to 
calculate the weight of a Part made with this Material.

We may need to add a 'strength' property to this class later.
"""
class Material:
    def __init__(self, name, density):
        self.name = name
        self.density = density
    def __str__(self):
        return "name = " + str(self.name) + ", density = " + str(self.density)

"""
Define the three available types of materials:
(1) wood/fabric
(2) composite
(3) metal

Assume the following densities:
wood density = 500 kg/m^3 (Pine, white; https://www.engineeringtoolbox.com/wood-density-d_40.html)
fabric density = 1560 kg/m^3 (cotton; https://en.wikipedia.org/wiki/Cotton#Fiber_properties)
wood/fabric density = 0.2*(wood density) + 0.8*(fabric density) = 1348 kg/m^3
composite density = 1744 kg/m^3 (CFRP: IM-7 PAN-Based Carbon; https://www.engineeringtoolbox.com/polymer-composite-fibers-d_1226.html)
metal density = 2700 kg/m^3 (aluminum; https://en.wikipedia.org/wiki/Aluminium)
"""
woodfabric = Material("wood/fabric", 1348)
composite = Material("composite", 1744)
metal = Material("metal", 2700)

# -----------------------------------------------------------------------------

"""
The class Part defines or calculates the five basic properties of an aircraft part:
(1) material
(2) lift
(3) weight
(4) thrust
(5) drag
"""
class Part:
    def __init__(self, material, volume, lift, thrust, drag):
        self.material = material
        # set the volume of this part (how big is it?)
        self.volume = volume
        self.lift = lift
        # calculate part weight from part volume and material density
        self.weight = volume*material.density
        self.thrust = thrust
        self.drag = drag
    def __str__(self):
        return ("material = [" + str(self.material) + "]" +
            "\nvolume = " + str(self.volume) + "," +
            "\nlift = " + str(self.lift) + "," +
            " weight = " + str(self.weight) + "," +
            " thrust = " + str(self.thrust) + "," +
            " drag = " + str(self.drag))


"""
The class Fuselage and its subclasses set up two specific kinds of parts:
(1) Narrow body fuselage
(2) Wide body fuselage
"""
class Fuselage(Part):
    def __init__(self, material, volume, lift, drag):
        """
        Fuselage (body of airplane).
        These don't make thrust, so set properties as:
        thrust = 0
        """
        Part.__init__(self, material, volume, lift, 0, drag)

class NarrowBody(Fuselage):
    def __init__(self, material):
        """
        Narrow body fuselage; user only needs to specify the material.
        Set other properties as:
        volume = 50
        lift = 0.05
        drag = 0.20
        """
        Fuselage.__init__(self, material, 50, 0.05, 0.20)

class WideBody(Fuselage):
    def __init__(self, material):
        """
        Wide body fuselage; user only needs to specify the material.
        Set other properties as:
        volume = 100
        lift = 0.10
        drag = 0.30
        """
        Fuselage.__init__(self, material, 100, 0.10, 0.30)


"""
The class Wing and its subclasses set up four specific kinds of parts:
(1) short straight wings
(2) long straight wings
(3) swept wings
(4) delta wings
"""
class Wing(Part):
    def __init__(self, material, volume, lift, drag):
        """
        Wing.
        These don't make thrust, so set properties as:
        thrust = 0
        """
        Part.__init__(self, material, volume, lift, 0, drag)

class ShortStraight(Wing):
    def __init__(self, material):
        """
        Short straight wing; user only needs to specify the material.
        Set other properties as:
        volume = 10
        lift = 0.70
        drag = 0.70
        """
        Wing.__init__(self, material, 10, 0.70, 0.70)

class LongStraight(Wing):
    def __init__(self, material):
        """
        Long straight wing; user only needs to specify the material.
        Set other properties as:
        volume = 15
        lift = 1.00
        drag = 0.60
        """
        Wing.__init__(self, material, 15, 1.00, 0.60)

class SweptBack(Wing):
    def __init__(self, material):
        """
        Swept back wing; user only needs to specify the material.
        Set other properties as:
        volume = 20
        lift = 0.85
        drag = 0.65
        """
        Wing.__init__(self, material, 20, 0.85, 0.65)

class Delta(Wing):
    def __init__(self, material):
        """
        Delta wing; user only needs to specify the material.
        Set other properties as:
        volume = 25
        lift = 0.60
        drag = 0.75
        """
        Wing.__init__(self, material, 25, 0.60, 0.75)


"""
The class Engine and its subclasses set up four specific kinds of parts:
(1) single propeller
(2) double propeller
(3) single jet
(4) double jet
"""
class Engine(Part):
    def __init__(self, material, volume, thrust, drag):
        """
        Engine.
        These don't make lift, so set properties as:
        lift = 0
        """
        Part.__init__(self, material, volume, 0, thrust, drag)

class SinglePropeller(Engine):
    def __init__(self, material):
        """
        Single propeller engine; user only needs to specify the material.
        Set other properties as:
        volume = 5
        thrust = 0.50
        drag = 0.10

        Assume this is like the propeller engine in a Pitts Special.
        power = 260 hp (194 kW)
        (ref: https://en.wikipedia.org/wiki/Pitts_Special#Specifications_(S-2B))
        propeller diameter = 78 in (1.98 m)
        (ref: https://hartzellprop.com/wp-content/uploads/159-0000-R66-WA.pdf, pg. 1487)
        propeller efficiency = 0.85
        (ref: https://aviation.stackexchange.com/questions/29611/how-to-calculate-the-thrust-of-a-piston-or-turboprop-engine)
        air density = 1.23 kg/m^3
        (ref: https://en.wikipedia.org/wiki/Density_of_air#Dry_air)
        thrust = (power^2 * efficiency^2 * pi/2 * diameter^2 * air_density)^(1/3)
        (ref: https://aviation.stackexchange.com/questions/29611/how-to-calculate-the-thrust-of-a-piston-or-turboprop-engine)
        """
        power = 194000 # W
        diameter = 1.98 # m
        efficiency = 0.85
        pi = 3.14
        air_density = 1.23 # kg/m^3
        thrust = (power**2.0 * efficiency**2.0 * pi/2.0 * diameter**2.0 * air_density)**(1.0/3.0) # N
        Engine.__init__(self, material, 5, thrust, 0.10)

class DoublePropeller(Engine):
    def __init__(self, material):
        """
        Dobule propeller engine; user only needs to specify the material.
        Set other properties as:
        volume = 10
        thrust = 0.70
        drag = 0.15

        Assume twice the thrust of SinglePropeller.
        """
        power = 194000 # W
        diameter = 1.98 # m
        efficiency = 0.85
        pi = 3.14
        air_density = 1.23 # kg/m^3
        thrust = (power**2.0 * efficiency**2.0 * pi/2.0 * diameter**2.0 * air_density)**(1.0/3.0) # N
        Engine.__init__(self, material, 10, thrust*2.0, 0.15)

class SingleJet(Engine):
    def __init__(self, material):
        """
        Single jet engine; user only needs to specify the material.
        Set other properties as:
        volume = 7
        thrust = 0.80
        drag = 0.05

        Assume this is like the J75 jet engine in an F-106.
        thrust = 17500 lbf (77.84 kN)
        (ref: https://en.wikipedia.org/wiki/Pratt_%26_Whitney_J75#Specifications_(JT4A-11))
        """
        Engine.__init__(self, material, 7, 77840, 0.05)

class DoubleJet(Engine):
    def __init__(self, material):
        """
        Double jet engine; user only needs to specify the material.
        Set other properties as:
        volume = 14
        thrust = 1.00
        drag = 0.10

        Assume twice the thrust of the SingleJet.
        """
        Engine.__init__(self, material, 14, 77840*2.0, 0.10)


# -----------------------------------------------------------------------------
"""
The class Airplane defines the four things a guest needs to pick to design a plane:
(1) material
(2) fuselage shape
(3) wing shape
(4) engine type
"""
class Airplane:
    def __init__(self, material, fuselage, wing, engine):
        # define material
        self.material = material
        # define fuselage
        if fuselage == "wide body":
            self.fuselage = WideBody(material)
        if fuselage == "narrow body":
            self.fuselage = NarrowBody(material)
        self.fuselage.name = fuselage
        # define wing
        if wing == "short straight":
            self.wing = ShortStraight(material)
        if wing == "long straight":
            self.wing = LongStraight(material)
        if wing == "swept back":
            self.wing = SweptBack(material)
        if wing == "delta":
            self.wing = Delta(material)
        self.wing.name = wing
        # define engine
        if engine == "single propeller":
            self.engine = SinglePropeller(material)
        if engine == "double propeller":
            self.engine = DoublePropeller(material)
        if engine == "single jet":
            self.engine = SingleJet(material)
        if engine == "double jet":
            self.engine = DoubleJet(material)
        self.engine.name = engine
        # calculate totals for performance
        self.volume = self.fuselage.volume + self.wing.volume + self.engine.volume
        self.lift = self.fuselage.lift + self.wing.lift + self.engine.lift
        self.weight = self.fuselage.weight + self.wing.weight + self.engine.weight
        self.thrust = self.fuselage.thrust + self.wing.thrust + self.engine.thrust
        self.drag = self.fuselage.drag + self.wing.drag + self.engine.drag
    def __str__(self):
        return ("material = [" + str(self.material) + "]" +
            "\nshape = [fuselage = " + str(self.fuselage.name) + "," +
            " wing = " + str(self.wing.name) + "," +
            " engine = " + str(self.engine.name) + "]" +
            "\nvolume = " + str(self.volume) + "," +
            "\nlift = " + str(self.lift) + "," +
            " weight = " + str(self.weight) + "," +
            " thrust = " + str(self.thrust) + "," +
            " drag = " + str(self.drag))
    def takeoff(self):
        thrust_drag_flag = False
        lift_weight_flag = False
        takeoff_flag = False
        if (self.thrust > self.drag):
            thrust_drag_flag = True
        if (self.lift > self.weight):
            lift_weight_flag = True
        if (thrust_drag_flag and lift_weight_flag):
            takeoff_flag = True
        return takeoff_flag


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # define all the different airplane materials and parts
    materials = (woodfabric, composite, metal)
    fuselages = ("narrow body", "wide body")
    wings = ("short straight", "long straight", "swept back", "delta")
    engines = ("single propeller", "double propeller", "single jet", "double jet")

    # create all combinations of individual parts, then save their properties
    parts = pd.DataFrame(columns=['class', 'part', 'material', 
        'lift', 'weight', 'thrust', 'drag', 'volume', 'density'])
    for fuselage in fuselages:
        for material in materials:
            # get fuselage properties
            if fuselage == "wide body":
                f = WideBody(material)
            if fuselage == "narrow body":
                f = NarrowBody(material)
            f.name = fuselage
            part_properties = pd.DataFrame({
                'class': ['fuselage'],
                'part': [f.name],
                'material': [material.name],
                'lift': [f.lift],
                'weight': [f.weight],
                'thrust': [f.thrust],
                'drag': [f.drag],
                'volume': [f.volume],
                'density': [material.density]})
            parts = parts.append(part_properties, ignore_index=True)
    for wing in wings:
        for material in materials:
            # get wing properties
            if wing == "short straight":
                w = ShortStraight(material)
            if wing == "long straight":
                w = LongStraight(material)
            if wing == "swept back":
                w = SweptBack(material)
            if wing == "delta":
                w = Delta(material)
            w.name = wing
            part_properties = pd.DataFrame({
                'class': ['wing'],
                'part': [w.name],
                'material': [material.name],
                'lift': [w.lift],
                'weight': [w.weight],
                'thrust': [w.thrust],
                'drag': [w.drag],
                'volume': [w.volume],
                'density': [material.density]})
            parts = parts.append(part_properties, ignore_index=True)
    for engine in engines:
        for material in materials:
            # get engine properties
            if engine == "single propeller":
                e = SinglePropeller(material)
            if engine == "double propeller":
                e = DoublePropeller(material)
            if engine == "single jet":
                e = SingleJet(material)
            if engine == "double jet":
                e = DoubleJet(material)
            e.name = engine
            part_properties = pd.DataFrame({
                'class': ['engine'],
                'part': [e.name],
                'material': [material.name],
                'lift': [e.lift],
                'weight': [e.weight],
                'thrust': [e.thrust],
                'drag': [e.drag],
                'volume': [e.volume],
                'density': [material.density]})
            parts = parts.append(part_properties, ignore_index=True)


    parts.to_csv('parts.csv', columns=['class', 'part', 'material', 
        'lift', 'weight', 'thrust', 'drag', 'volume', 'density'], index=False)


    # create all 96 combinations of airplanes with different materials and parts
    # then, simulate each of their takeoffs and save the results
    planes = pd.DataFrame(columns=['material', 'fuselage', 'wing', 'engine',
        'total lift', 'total weight', 'total thrust', 'total drag',
        'successful takeoff?'])
    for material in materials:
        for engine in engines:
            for wing in wings:
                for fuselage in fuselages:
                    # create airplane
                    airplane = Airplane(material, fuselage, wing, engine)
                    # simulate takeoff
                    plane_results = pd.DataFrame({
                        'material': [material.name],
                        'fuselage': [fuselage],
                        'wing': [wing],
                        'engine': [engine],
                        'total lift': [airplane.lift],
                        'total weight': [airplane.weight],
                        'total thrust': [airplane.thrust],
                        'total drag': [airplane.drag],
                        'successful takeoff?': [airplane.takeoff()]
                        })
                    planes = planes.append(plane_results, ignore_index=True)

    planes.to_csv('planes.csv', columns=['fuselage', 'wing', 'engine', 'material', 
        'total lift', 'total weight', 'total thrust', 'total drag', 
        'successful takeoff?'], index=False)
