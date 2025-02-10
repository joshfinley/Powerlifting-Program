from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import calendar
import os

class Exercise:
    def __init__(self, name: str, sets: int, reps: int, intensity: float):
        self.name = name
        self.sets = sets
        self.reps = reps
        self.intensity = intensity

class PowerliftingProgram:
    def __init__(self):
        # Force the date to be Monday, February 10th, 2025
        self.start_date = datetime(year=2025, month=2, day=10, hour=0, minute=0, second=0, microsecond=0)
        self.bars = ["SSB", "Cambered", "Straight"]
        self.current_bar_index = 0
        self.weeks_on_current_bar = 0
        
        # Verify the start date is correct
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
            1: Exercise("Squat", 2, 15, 0.625),
            2: Exercise("Squat", 3, 7, 0.76),
            3: Exercise("Squat", 4, 3, 0.86),
            4: Exercise("Box Squat", 1, 1, 1.0)
        }
        return progressions[week_in_cycle]
    
    def get_gear_level(self, week_in_cycle: int) -> str:
        """Returns gear requirements - only used on peak week"""
        return "Suit + Briefs" if week_in_cycle == 4 else "Raw"
    
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
            1: (2, 15, 0.625),
            2: (3, 7, 0.76),
            3: (4, 3, 0.86),
            4: (1, 1, 1.0)
        }
        sets, reps, intensity = intensities[week_in_cycle]
        return f"{style}: {sets}x{reps} @ {intensity*100}%"
    
    def get_bench_workout(self, week_in_cycle: int) -> str:
        """Returns bench workout based on week in cycle"""
        bench_progression = {
            1: "Bench Press: 2x15 @ 62.5%",
            2: "Bench Press: 3x7 @ 76%",
            3: "Bench Press: 4x3 @ 86%",
            4: "Bench Press (Shirted): 1x1 @ 100%"
        }
        return bench_progression[week_in_cycle]

    def generate_week(self, week_number: int) -> Dict:
        """Generates a full week of programming"""
        week_in_cycle = ((week_number - 1) % 4) + 1
        month = ((week_number - 1) // 4) + 1
        current_bar = self.get_bar_for_week(week_number)
        chains = self.get_chain_status(week_number)
        gear = self.get_gear_level(week_in_cycle)
        deadlift_style = self.get_deadlift_style(month)
        week_date = self.get_week_date(week_number)
        
        squat = self.get_squat_progression(week_in_cycle)
        
        week_program = {
            "Date": week_date.strftime('%m-%d-%Y'),
            "Week": week_number,
            "Bar Type": current_bar,
            "Chains": chains,
            "Gear": gear,
            "Monday": {
                "Main": f"{squat.name}: {squat.sets}x{squat.reps} @ {squat.intensity*100}% {gear if gear != 'Raw' else ''}",
                "Accessories": [
                    "Lunges: 4x15",
                    "Heel Touch Step Downs: 3x15",
                    "Giant Set (5 rounds):",
                    "- Cable Woodchopper: AMRAP",
                    "- Seated Barbell OHP: 12 reps",
                    "- T-bar Row: 12 reps"
                ]
            },
            "Wednesday": {
                "Cardio": self.get_cardio_workout(week_number)
            },
            "Friday": {
                "Main": self.get_deadlift_workout(week_in_cycle, deadlift_style),
                "Giant Set": [
                    "Weighted Decline Situps: AMRAP",
                    "Bench Press: AMRAP @ 65%",
                    "Lat Pulldown: 12 reps"
                ]
            },
            "Sunday": {
                "Main": self.get_bench_workout(week_in_cycle),
                "Accessories": [
                    "JM Press: 4x12",
                    "Incline DB Press: 3x12",
                    "Superset (5 rounds):",
                    "- Long Rope Tricep Pushdown",
                    "- Rear Delt Flies"
                ]
            }
        }
        return week_program
    
    def format_week_to_string(self, week_program: Dict) -> str:
        """Formats a week's program as a string"""
        output = []
        output.append(f"Week {week_program['Week']} - {week_program['Date']}")
        output.append(f"Bar: {week_program['Bar Type']}")
        output.append(f"Chains: {'Yes' if week_program['Chains'] else 'No'}")
        output.append(f"Gear: {week_program['Gear']}\n")
        
        for day, workout in week_program.items():
            if day not in ['Week', 'Bar Type', 'Chains', 'Gear', 'Date']:
                output.append(f"{day}:")
                if isinstance(workout, dict):
                    for key, value in workout.items():
                        if isinstance(value, list):
                            output.append(f"{key}:")
                            for item in value:
                                output.append(f"  {item}")
                        else:
                            output.append(f"{key}: {value}")
                else:
                    output.append(workout)
                output.append("")
        
        return "\n".join(output)
    
    def format_week_to_html(self, week_program: Dict) -> str:
        """Formats a week's program as HTML"""
        html = f"""
        <div class="week-program">
            <div class="week-header">
                <h2>Week {week_program['Week']} - {week_program['Date']}</h2>
                <div class="program-meta">
                    <p><strong>Bar:</strong> {week_program['Bar Type']}</p>
                    <p><strong>Chains:</strong> {'Yes' if week_program['Chains'] else 'No'}</p>
                    <p><strong>Gear:</strong> {week_program['Gear']}</p>
                </div>
            </div>
        """
        
        for day, workout in week_program.items():
            if day not in ['Week', 'Bar Type', 'Chains', 'Gear', 'Date']:
                html += f'<div class="workout-day"><h3>{day}</h3>'
                if isinstance(workout, dict):
                    for key, value in workout.items():
                        if isinstance(value, list):
                            html += f'<div class="workout-section"><h4>{key}:</h4><ul>'
                            for item in value:
                                if item.startswith('-'):
                                    html += f'<li class="sub-item">{item[2:]}</li>'
                                else:
                                    html += f'<li>{item}</li>'
                            html += '</ul></div>'
                        else:
                            html += f'<div class="workout-section"><h4>{key}:</h4><p>{value}</p></div>'
                else:
                    html += f'<p>{workout}</p>'
                html += '</div>'
        
        html += '</div>'
        return html
    
    def generate_css(self) -> str:
        """Generates CSS styling for the program"""
        return """
        <style>
            .week-program {
                max-width: 800px;
                margin: 20px auto;
                padding: 20px;
                font-family: Arial, sans-serif;
                background-color: #ffffff;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                border-radius: 8px;
            }
            .week-header {
                border-bottom: 2px solid #eee;
                margin-bottom: 20px;
                padding-bottom: 10px;
            }
            .program-meta {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 10px;
                margin: 10px 0;
            }
            .workout-day {
                margin: 20px 0;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 6px;
            }
            .workout-day h3 {
                color: #2c3e50;
                margin-top: 0;
                border-bottom: 1px solid #dee2e6;
                padding-bottom: 8px;
            }
            .workout-section {
                margin: 15px 0;
            }
            .workout-section h4 {
                color: #495057;
                margin: 10px 0 5px 0;
            }
            ul {
                list-style-type: none;
                padding-left: 0;
            }
            li {
                margin: 5px 0;
                padding: 5px 0;
            }
            .sub-item {
                padding-left: 20px;
                color: #666;
            }
            p {
                margin: 5px 0;
            }
        </style>
        """
    
    def generate_html_file(self, week_program: Dict, filename: str) -> None:
        """Generates a complete HTML file for a week's program"""
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Powerlifting Program - Week {week_program['Week']}</title>
            {self.generate_css()}
        </head>
        <body>
            {self.format_week_to_html(week_program)}
        </body>
        </html>
        """
        
        with open(filename, 'w') as f:
            f.write(html_content)

    def generate_index_html(self, programs: List[Dict]) -> str:
        """Generates an index.html file linking to all program weeks"""
        links_html = ""
        for program in programs:
            week_num = program["Week"]
            date = program["Date"]
            filename = f"docs/{date}-program.html"  # Fixed line
            links_html += f'<li><a href="{filename}">Week {week_num} - {date}</a></li>'

        index_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>6-Month Powerlifting Program</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 40px auto;
                    padding: 0 20px;
                }}
                .program-index {{
                    background: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 2px solid #eee;
                    padding-bottom: 10px;
                }}
                ul {{
                    list-style-type: none;
                    padding: 0;
                }}
                li {{
                    margin: 10px 0;
                    padding: 10px;
                    background: #f8f9fa;
                    border-radius: 4px;
                }}
                a {{
                    color: #2c3e50;
                    text-decoration: none;
                }}
                a:hover {{
                    color: #3498db;
                }}
            </style>
        </head>
        <body>
            <div class="program-index">
                <h1>6-Month Powerlifting Program</h1>
                <ul>
                    {links_html}
                </ul>
            </div>
        </body>
        </html>
        """
        return index_html

    def generate_and_save_program(self) -> None:
        """Generates the full 6-month program and saves each week as an HTML file"""
        total_weeks = 24  # 6 months
        
        # Use docs directory for GitHub Pages
        if not os.path.exists("docs"):
            os.makedirs("docs")
        
        print(f"Program start date: {self.start_date.strftime('%m-%d-%Y')}")
        
        # Store all programs to generate index
        all_programs = []
        
        for week in range(1, total_weeks + 1):
            current_date = self.start_date + timedelta(days=7 * (week - 1))
            print(f"Week {week}: {current_date.strftime('%m-%d-%Y')}")
            
            week_program = self.generate_week(week)
            all_programs.append(week_program)
            
            filename = f"docs/{current_date.strftime('%m-%d-%Y')}-program.html"
            self.generate_html_file(week_program, filename)
        
        # Generate index.html
        index_html = self.generate_index_html(all_programs)
        with open("index.html", "w") as f:
            f.write(index_html)


if __name__ == "__main__":
    program = PowerliftingProgram()
    program.generate_and_save_program()