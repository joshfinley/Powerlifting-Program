# main.py
import os
from typing import List, Dict
import markdown
from program_builder import ProgramBuilder
from html_templates import HTMLTemplates

class ProgramGenerator:
    def __init__(self, total_weeks: int = 24):
        self.program_builder = ProgramBuilder()
        self.total_weeks = total_weeks
        self.output_dir = "docs"
        
    def ensure_output_directory(self):
        """Ensures the output directory exists"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
    def generate_all_programs(self) -> List[Dict]:
        """Generates program data for all weeks"""
        return [
            self.program_builder.build_week(week) 
            for week in range(1, self.total_weeks + 1)
        ]
        
    def generate_index_page(self, all_programs: List[Dict]) -> str:
        """Generates the index.html content"""
        # Generate week links for sidebar
        links_html = ""
        for program in all_programs:
            week_num = program["Week"]
            date = program["Date"]
            links_html += f'<li><a href="{date}-program.html">Week {week_num} - {date}</a></li>'

        # Parse README.md if it exists
        try:
            with open('README.md', 'r', encoding='utf-8') as f:
                readme_content = f.read()
            
            md = markdown.Markdown(extensions=[
                'extra',
                'codehilite',
                'meta'
            ])
            readme_html = md.convert(readme_content)
        except FileNotFoundError:
            readme_html = "<p>Program documentation not found.</p>"

        return f"""
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
    
    def generate_program(self):
        """Main method to generate all program files"""
        print(f"Program start date: {self.program_builder.start_date.strftime('%m-%d-%Y')}")
        
        # Ensure output directory exists
        self.ensure_output_directory()
        
        # Generate all program data
        all_programs = self.generate_all_programs()
        
        # Generate individual program pages
        for program in all_programs:
            filename = f"{self.output_dir}/{program['Date']}-program.html"
            html_content = HTMLTemplates.generate_program_page(program, all_programs)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"Generated program for Week {program['Week']}: {program['Date']}")
        
        # Generate index page
        index_html = self.generate_index_page(all_programs)
        with open(f"{self.output_dir}/index.html", 'w', encoding='utf-8') as f:
            f.write(index_html)
        
        print(f"\nGenerated {len(all_programs)} weeks of programming")
        print(f"Files saved to: {os.path.abspath(self.output_dir)}")

def main():
    generator = ProgramGenerator()
    generator.generate_program()

if __name__ == "__main__":
    main()