from resources.resource import Resource

RESOURCE_CATALOG = {
    "Layer 1": {
        "Surface Resources": {},
        "Forest Resources": {},
        "Grassland Resources": {},
        "River Resources": {},
        "Lake Resources": {},
        "Swamp Resources": {},
        "Mountain Resources": {},
        "Hill Resources": {},
        "Desert Resources": {},
        "Coastal Resources": {},
        "Ocean Resources": {},
        "Volcanic Resources": {},
        "Arctic / Tundra Resources": {},
        "Ruins Resources": {},
        "Island Resources": {}
    },

        
    "Layer 2": {
        "Stone and Construction Minerals": {},
        "Metal Ores": {},
        "Precious Metals": {},
        "Gemstones": {},
        "Industrial Minerals": {},
        "Chemical Minerals": {},
        "Fossil Fuels": {},
        "Groundwater": {},
        "Rare Earth Elements": {},
        "Radioactive Materials": {},
        "Agriculture": {},
        "Horticulture": {},
        "Forestry": {},
        "Fisheries": {},
        "Dairy": {},
        "Livestock Products": {}
    }

    "Layer 3": {
        "Construction Materials": {},
        "Mechanical Components": {},
        "Electrical Components": {},
        "Chemical Products": {},
        "Textiles": {},
        "Food Products": {},
        "Medical Products": {},
        "Energy Products": {},
        "Transportation Products": {},
        "Weapon Assemblies": {},
        "Communication Products": {},
        "Scientific Experiments": {},
        "Scientific Assistance": {},
        "Space Products": {},
        "Financial Parts": {},
        "Others": {}
    }

    "Layer 4": {
        "Basic Knowledge": {},
        "Engineering Knowledge": {},
        "Scientific Knowledge": {},
        "Agricultural Knowledge": {},
        "Medical Knowledge": {},
        "Construction Knowledge": {},
        "Mechanical Knowlegde": {},
        "Electrical Knowledge": {},
        "Chemical Knowledge": {},
        "Biological Knowledge": {},
        "Computing Knowledge": {},
        "Military Strategy": {},
        "Economic Knowledge": {},
        "Transportation Knowledge": {},
        "History Knowledge": {},
        "Geographical Knowledge": {},
        "Space Knowledge": {},
        "Civic Knowlegde":{}
    }
}

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

RESOURCE_CATALOG["Layer 2"]["Metal Ores"]["Iron Ore"] = iron_ore