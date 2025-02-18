from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import calendar

class Exercise:
    def __init__(self, name: str, sets: int, reps: int, intensity: float, is_amrap: bool = False):
        self.name = name
        self.sets = sets
        self.reps = reps
        self.intensity = intensity
        self.is_amrap = is_amrap