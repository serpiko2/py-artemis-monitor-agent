class PropertiesServiceParameters:

    def __init__(self,
                 service_properties,
                 interface,
                 name):
        self.service_properties = service_properties
        self.interface = interface
        self.name = name

    def __hash__(self) -> int:
        return hash((self.service_properties, self.interface, self.name))

    def __eq__(self, other) -> bool:
        if not isinstance(other, PropertiesServiceParameters):
            return NotImplemented
        return (
            (self.service_properties, self.interface, self.name) ==
            (other.service_properties, other.interface, other.name))
