from rynput import Property, PropertyGroup, validators

properties = PropertyGroup([
    Property("RegEx", validators.RegEx(r"[abc123 ]+")),
    Property("Bool", validators.Bool(), True),
    Property("Option", validators.Option(["Foo", "Bar", "Baz"]), "Foo"),
    Property("Integer", validators.Integer(4, 8)),
    Property("Float", validators.Float(), 3.1415)
])

def main():
    values = properties.values_from_input()
    for key in values:
        print(key, ":", values[key])

main()