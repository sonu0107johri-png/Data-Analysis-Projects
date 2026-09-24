from resources.resource import Resource

def main():
    iron_ore = Resource(
        name="Iron Ore",
        layer=2,
        category="Metal Ores",
        quantity=500,
        quality=3,
        biome_availability=[
            "Mountain Resources",
            "Hill Resources"
        ],
        renewable=False,
        uses=[
            "Iron Production",
            "Construction",
            "Machine Manufacturing",
            "Weapon Designing"
        ],
        trade_value=25,
        rarity="Common",
        required_technology="Basic Mining"
    )

    iron_ore.display_details()

if __name__ == "__main__":
    main()