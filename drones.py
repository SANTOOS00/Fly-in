from typing import Any, List, Dict


class Drones:
    def __init__(self, number_drones: int) -> None:
        self.drones: List[Dict[str, Any]] = [
            {
                "id": num + 1,
                "name_zome": None,
                "zone_visited": [],
            }
            for num in range(number_drones)
            ]
