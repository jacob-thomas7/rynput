from rynput import Property, PropertyGroup, validators
import json

properties = PropertyGroup([
    Property("RegEx", validators.RegEx(r"[abc123 ]+")),
    Property("Bool", validators.Bool(), True),
    Property("Option", validators.Option(["Foo", "Bar", "Baz"]), "Foo"),
    Property("Integer", validators.Integer(4, 8), desc="An integer"),
    Property("Float", validators.Float(), 3.1415)
])

def main():
    with open("example.json", "r") as config_file:
        config_data = json.load(config_file)
        
        values = properties.values_from_dict(config_data)
        for key in values:
            print(key, ":", values[key])

main()