from enum import Enum 

class Type_zone(Enum):
    NORMAL = (1, 'normal'),
    PRIORITY = (1, 'priority'),
    RESTRICTED = (2, 'restricted'),
    BLOCKED = (float('inf'), 'blocked'),


# for stat in Type_zone:
#     print(stat)