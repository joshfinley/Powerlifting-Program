from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import calendar
import os

class Exercise:
    def __init__(self, name: str, sets: int, reps: int, intensity: float, is_amrap: bool = False):
        self.name = name
        self.sets = sets
        self.reps = reps
        self.intensity = intensity
        self.is_amrap = is_amrap

class PowerliftingProgram:
    def __init__(self):
        # Force the date to be Monday, February 10th, 2025
        self.start_date = datetime(year=2025, month=2, day=17, hour=0, minute=0, second=0, microsecond=0)
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
            1: Exercise("Squat", 2, 15, 0.625, is_amrap=True),
            2: Exercise("Squat", 3, 7, 0.76),
            3: Exercise("Squat", 4, 3, 0.86),
            4: Exercise("Box Squat", 1, 1, "RPE 9-10")
        }
        return progressions[week_in_cycle]
        
        
    def get_gear_level(self, week_number: int) -> str:
        """Returns gear requirements - peak weeks follow 3-month cycle of briefs->suit->briefs+suit"""
        week_in_cycle = ((week_number - 1) % 4) + 1
        if week_in_cycle != 4:  # Only use gear on week 4 of each cycle
            return "Raw"
            
        # On peak weeks (week 4), cycle through gear every 3 months (12 weeks)
        peak_count = (week_number - 1) // 4  # How many peak weeks have passed (0-based)
        gear_cycle = peak_count % 3  # 0=briefs, 1=suit, 2=briefs+suit
        
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

    def generate_week(self, week_number: int) -> Dict:
        """Generates a full week of programming"""
        week_in_cycle = ((week_number - 1) % 4) + 1
        month = ((week_number - 1) // 4) + 1
        current_bar = self.get_bar_for_week(week_number)
        gear = self.get_gear_level(week_number)
        deadlift_style = self.get_deadlift_style(month)
        week_date = self.get_week_date(week_number)
        
        squat = self.get_squat_progression(week_in_cycle)
        reps_display = f"{squat.reps}+" if squat.is_amrap else str(squat.reps)
        intensity_display = f"{squat.intensity*100}%" if isinstance(squat.intensity, float) else squat.intensity
            
        week_program = {
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
                    "Weighted Decline Situps: AMRAP",
                    "Bench Press: AMRAP @ 65%",
                    "Lat Pulldown: 12 reps"
                ]
            },
        }
        return week_program
    
    def format_week_to_string(self, week_program: Dict) -> str:
        """Formats a week's program as a string"""
        output = []
        output.append(f"Week {week_program['Week']} - {week_program['Date']}")
        output.append(f"Bar: {week_program['Bar Type']}")
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
        """Generates an index.html file with program overview and links to all program weeks"""
        # Generate week links
        links_html = ""
        for program in programs:
            week_num = program["Week"]
            date = program["Date"]
            filename = f"docs/{date}-program.html"
            links_html += f'<li><a href="{filename}">Week {week_num} - {date}</a></li>'

        # Read and parse README.md content
        try:
            import markdown
            from markdown.extensions.fenced_code import FencedCodeExtension
            from markdown.extensions.tables import TableExtension
            
            with open('README.md', 'r', encoding='utf-8') as f:
                readme_content = f.read()
                
            # Convert markdown to HTML with extensions
            md = markdown.Markdown(extensions=[
                'extra',  # includes tables, fenced_code, footnotes, and more
                'codehilite',  # syntax highlighting
                'meta'  # metadata processing
            ])
            readme_html = md.convert(readme_content)
            
        except ImportError:
            readme_html = "<p>Please install the 'markdown' package to render README content.</p>"
        except FileNotFoundError:
            readme_html = "<p>README.md file not found.</p>"

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
                    max-width: 1200px;
                    margin: 40px auto;
                    padding: 0 20px;
                    line-height: 1.6;
                }}
                .program-container {{
                    display: grid;
                    grid-template-columns: 250px 1fr;
                    gap: 30px;
                    margin-top: 30px;
                }}
                .sidebar {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    height: fit-content;
                    position: sticky;
                    top: 20px;
                }}
                .main-content {{
                    background: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h1, h2, h3 {{
                    color: #2c3e50;
                }}
                h1 {{
                    border-bottom: 2px solid #eee;
                    padding-bottom: 10px;
                }}
                h2 {{
                    margin-top: 30px;
                    border-bottom: 1px solid #eee;
                    padding-bottom: 5px;
                }}
                .week-links {{
                    list-style-type: none;
                    padding: 0;
                }}
                .week-links li {{
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
                /* README content styles */
                .readme-content {{
                    margin-top: 20px;
                }}
                .readme-content h1 {{
                    font-size: 2em;
                    margin-top: 0;
                }}
                .readme-content h2 {{
                    font-size: 1.5em;
                    margin-top: 25px;
                }}
                .readme-content h3 {{
                    font-size: 1.2em;
                    margin-top: 20px;
                }}
                .readme-content p {{
                    margin: 15px 0;
                }}
                .readme-content ul, .readme-content ol {{
                    padding-left: 25px;
                    margin: 15px 0;
                }}
                .readme-content li {{
                    margin: 5px 0;
                }}
                .readme-content code {{
                    background-color: #f6f8fa;
                    padding: 2px 4px;
                    border-radius: 3px;
                    font-family: monospace;
                }}
                .readme-content pre {{
                    background-color: #f6f8fa;
                    padding: 16px;
                    border-radius: 6px;
                    overflow-x: auto;
                }}
                .readme-content blockquote {{
                    margin: 15px 0;
                    padding: 0 15px;
                    border-left: 4px solid #ddd;
                    color: #666;
                }}
                .readme-content table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 15px 0;
                }}
                .readme-content th, .readme-content td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                .readme-content th {{
                    background-color: #f6f8fa;
                }}
            </style>
        </head>
        <body>
            <h1>6-Month Powerlifting Program</h1>
            
            <div class="program-container">
                <div class="sidebar">
                    <h3>Quick Navigation</h3>
                    <ul class="week-links">
                        {links_html}
                    </ul>
                </div>
                
                <div class="main-content">
                    <div class="readme-content">
                        {readme_html}
                    </div>
                </div>
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