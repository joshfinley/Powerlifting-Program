from datetime import datetime, timedelta
from typing import Dict, List, Optional
from models import Exercise

class ProgramBuilder:
    def __init__(self):
        self.start_date = datetime(year=2025, month=2, day=17, hour=0, minute=0, second=0, microsecond=0)
        self.bars = ["SSB", "Cambered", "Straight"]
        
        if self.start_date.weekday() != 0:  # 0 is Monday
            raise ValueError(f"Start date {self.start_date.strftime('%m-%d-%Y')} is not a Monday")
    
    def get_week_date(self, week_number: int) -> datetime:
        """Calculate the date for a given week number"""
        week_date = self.start_date + timedelta(days=7 * (week_number - 1))
        return week_date.replace(hour=0, minute=0, second=0, microsecond=0)
        
    def get_bar_for_week(self, week_number: int) -> str:
        """Returns which bar to use based on 8-week cycles"""
        bar_cycle = (week_number - 1) // 8
        return self.bars[bar_cycle % 3]
    
    def get_chain_status(self, week_number: int) -> bool:
        """Returns whether chains should be used this week based on monthly rotation"""
        month = ((week_number - 1) // 4) + 1
        if week_number % 4 == 0:  # Week 4 is always free weight
            return False
        return month % 2 == 1  # Alternate chains monthly
    
    def get_squat_progression(self, week_in_cycle: int) -> Exercise:
        """Returns squat parameters for given week in 4-week cycle"""
        progressions = {
            1: Exercise("Squat", 2, 15, 0.625, is_amrap=True),
            2: Exercise("Squat", 3, 7, 0.76),
            3: Exercise("Squat", 4, 3, 0.86),
            4: Exercise("Box Squat", 1, 1, "RPE 9-10")
        }
        return progressions[week_in_cycle]
    
    def get_gear_level(self, week_number: int) -> str:
        """Returns gear requirements based on 3-month cycle"""
        week_in_cycle = ((week_number - 1) % 4) + 1
        if week_in_cycle != 4:
            return "Raw"
            
        peak_count = (week_number - 1) // 4
        gear_cycle = peak_count % 3
        gear_types = ["Briefs", "Suit", "Briefs + Suit"]
        return gear_types[gear_cycle]
    
    def get_cardio_workout(self, week_number: int, weather_condition: str = "good") -> str:
        """Returns cardio workout based on week rotation and weather"""
        if weather_condition.lower() == "bad":
            return "Row ERG - 1 hour"
        workouts = ["Sled Drag", "Light Farmers Carry", "Ruck (25 lbs max)"]
        return f"{workouts[week_number % 3]} - 1 hour"
    
    def get_deadlift_style(self, month: int) -> str:
        """Returns deadlift style based on month"""
        return "Deficit Deadlift" if month % 2 == 0 else "Deadlift"

    def get_deadlift_workout(self, week_in_cycle: int, style: str) -> str:
        """Returns deadlift workout based on week in cycle and style"""
        intensities = {
            1: (2, 15, 0.625, True),
            2: (3, 7, 0.76, False),
            3: (4, 3, 0.86, False),
            4: (1, 1, "RPE 9-10", False)
        }
        sets, reps, intensity, is_amrap = intensities[week_in_cycle]
        reps_display = f"{reps}+" if is_amrap else str(reps)
        intensity_display = f"{intensity*100}%" if isinstance(intensity, float) else intensity
        return f"{style}: {sets}x{reps_display} @ {intensity_display}"
    
    def get_bench_workout(self, week_in_cycle: int) -> str:
        """Returns bench workout based on week in cycle"""
        bench_progression = {
            1: "Bench Press: 2x15 @ 62.5%",
            2: "Bench Press: 3x7 @ 76%",
            3: "Bench Press: 4x3 @ 86%",
            4: "Bench Press (Shirted): 1x1 @ RPE 9-10"
        }
        return bench_progression[week_in_cycle]

    def build_week(self, week_number: int) -> Dict:
        """Builds a full week of programming data structure"""
        week_in_cycle = ((week_number - 1) % 4) + 1
        month = ((week_number - 1) // 4) + 1
        current_bar = self.get_bar_for_week(week_number)
        gear = self.get_gear_level(week_number)
        deadlift_style = self.get_deadlift_style(month)
        week_date = self.get_week_date(week_number)
        
        squat = self.get_squat_progression(week_in_cycle)
        reps_display = f"{squat.reps}+" if squat.is_amrap else str(squat.reps)
        intensity_display = f"{squat.intensity*100}%" if isinstance(squat.intensity, float) else squat.intensity
            
        return {
            "Date": week_date.strftime('%m-%d-%Y'),
            "Week": week_number,
            "Bar Type": current_bar,
            "Gear": gear,
            "Sunday": {
                "Cardio": self.get_cardio_workout(week_number)
            },
            "Tuesday": {
                "Main": f"{squat.name}: {squat.sets}x{reps_display} @ {intensity_display} {gear if gear != 'Raw' else ''}",
                "Accessories": [
                    "Lunges: 4x15",
                    "Heel Touch Step Downs: 3x15",
                    "Giant Set (3-5 rounds):",
                    "- Cable Woodchopper: 15 reps",
                    "- Seated Barbell OHP: 12 reps",
                    "- T-bar Row: 12 reps"
                ]
            },
            "Wednesday": {
                "Main": self.get_bench_workout(week_in_cycle),
                "Accessories": [
                    "JM Press: 4x12",
                    "Dumbbell Bench Press: 3x15",
                    "Incline DB Press: 3x15",
                    "Superset (3-5 rounds):",
                    "- Long Rope Tricep Pushdown: 15 reps",
                    "- Rear Delt Flies or Cable Face Pull: 25 reps"
                ]
            },
            "Friday": {
                "Main": self.get_deadlift_workout(week_in_cycle, deadlift_style),
                "Accessories": [
                    "Hamstring Curl: 4x15",
                    "Reverse Hyper: 3x20"
                ],
                "Giant Set (3-5 Rounds)": [
                    "- Weighted Decline Situps: AMRAP",
                    "- Bench Press: AMRAP @ 65%",
                    "- Lat Pulldown: 12 reps"
                ]
            }
        }
