from enum import Enum

class Age_limits(str, Enum):
    ALL_AGES = '0+'
    KIDS_FROM_6_TO_12 = '6+'
    KIDS_FROM_12_TO_16 = '12+'
    KIDS_FROM_16_TO_18 = '16+'
    ADULTS = '18+'