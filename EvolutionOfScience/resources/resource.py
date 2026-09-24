class Resource:
    """
    Represents one resource used by the civilisation.
    """

    def __init__(
        self, 
        name, 
        layer, 
        category, 
        quantity=0, 
        quality=1, 
        biome_availability=None, 
        renewable=False,
        uses=None,
        trade_value=0,
        rarity="Common",
        required_technology=None
    ):
        self.name = name
        self.layer = layer
        self.category = category
        self.quantity = quantity
        self.quality = quality

        self.biome_availability = biome_availability or []
        self.renewable = renewable
        self.uses = uses or []

        self.trade_value = trade_value
        self.rarity = rarity
        self.required_technology = required_technology

    def display_details(self):
        print(f"Resource Name: {self.name}")
        print(f"Resource Layer: {self.layer}")
        print(f"Resource Category: {self.category}")
        print(f"Available Quantity: {self.quantity}")
        print(f"Quality Grade: {self.quality}")

        print(
            "Biome Availability: "
            f"{', '.join(self.biome_availability) or 'Not Assigned'}"
        )

        print(
            f"Renewable: {'Yes' if self.renewable else 'No'}"
        )
        print(f"Uses: {', '.join(self.uses) or 'Not Assigned'}")
        print(f"Trade Value: {self.trade_value}")
        print(f"Rarity: {self.rarity}")

        print(
            "Required Technology: "
            f"{self.required_technology or 'None'}"
        )