import os

base_dir = r"d:\Anti gravity llm\CityLink"

directories = [
    r"backend\citylink",
    r"backend\api",
    r"backend\sumo\network",
    r"backend\sumo\routes",
    r"backend\sumo\pedestrians",
    r"backend\sumo\configuration",
    r"unity\CityLinkUnity\Assets\Scripts",
    r"unity\CityLinkUnity\Assets\Prefabs",
    r"unity\CityLinkUnity\Assets\Materials",
    r"unity\CityLinkUnity\Assets\Models",
    r"unity\CityLinkUnity\Assets\Animations",
    r"unity\CityLinkUnity\Assets\Scenes",
    r"unity\CityLinkUnity\Assets\Textures",
    r"dashboard\src\components",
    r"dashboard\src\assets",
    r"dashboard\public",
    r"data",
    r"docs",
    r"scripts"
]

for d in directories:
    full_path = os.path.join(base_dir, d)
    os.makedirs(full_path, exist_ok=True)
    print(f"Created: {full_path}")

print("Directory structure created successfully.")
