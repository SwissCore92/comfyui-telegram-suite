from pathlib import Path

# This script is for automatically generate the converters.py file.
# Add more types here if needed.
TYPES = [
    "INT", 
    "FLOAT", 
    "BOOLEAN", 
    "STRING", 
    "DICT",
    "MODEL", 
    "CLIP", 
    "VAE", 
    "IMAGE", 
    "AUDIO",
    "LATENT",
]

def main():
    script = """
class AnyToX:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "any": ("*",),
            },
        }
    
    FUNCTION = "convert"
    CATEGORY = "Telegram Suite 🔽/converters"

    def convert(self, any):
        return (any,)
""" 

    type_mapping = []
    name_mapping = []

    for t in TYPES:
        type_mapping.append(f"\"AnyTo{t}\": AnyTo{t},")
        type_mapping.append(f"\"{t}ToAny\": {t}ToAny,")
        name_mapping.append(f"\"AnyTo{t}\": \"Any To {t}\",")
        name_mapping.append(f"\"{t}ToAny\": \"{t} To Any\",")

        script += f"""
class AnyTo{t}(AnyToX):
    RETURN_TYPES = ("{t}",)
    RETURN_NAMES = ("{t}",)

class {t}ToAny:
    @classmethod
    def INPUT_TYPES(cls):
        return {{
            "required": {{
                f"{t}": (f"{t}", {{"forceInput": True}}),
            }},
        }}
    FUNCTION = "convert"
    CATEGORY = "Telegram Suite 🔽/converters"

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("any",)

    def convert(self, {t}):
        return ({t},)
"""
    script += "\ntype_mapping = {\n    " + "\n    ".join([l for l in type_mapping]) + "\n}"
    script += "\nname_mapping = {\n    " + "\n    ".join([l for l in name_mapping]) + "\n}"

    with (Path(__file__).parent.parent / "nodes" / "converters.py").open("w", encoding="utf-8") as f:
        f.write(script)

if __name__ == "__main__":
    main()
