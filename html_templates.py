from typing import Dict, List
import markdown
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension

class HTMLTemplates:
    @staticmethod
    def generate_css() -> str:
        """Generates CSS styling for the program"""
        return """
        <style>
            /* Program container layout */
            .program-container {
                display: grid;
                grid-template-columns: 250px 1fr;
                gap: 30px;
                margin-top: 30px;
                width: 100%;
            }

            /* Base styles */
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 20px;
            }
            
            h1 {
                margin-bottom: 30px;
            }
            
            h1 a {
                color: #2c3e50;
                text-decoration: none;
            }
            
            h1 a:hover {
                color: #3498db;
            }
            
            /* Program styles */
            .week-program {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #ffffff;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                border-radius: 8px;
            }
            
            /* Navigation styles */
            .program-navigation {
                margin-bottom: 20px;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 6px;
                border: 1px solid #dee2e6;
            }
            
            .week-links {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 15px;
            }
            
            .week-select {
                padding: 8px 12px;
                border-radius: 4px;
                border: 1px solid #dee2e6;
                flex-grow: 1;
                max-width: 300px;
                font-size: 14px;
            }
            
            .nav-link {
                padding: 8px 16px;
                background-color: #e9ecef;
                border-radius: 4px;
                color: #495057;
                text-decoration: none;
                font-weight: 500;
                transition: all 0.2s ease;
            }
            
            .nav-link:hover {
                background-color: #dee2e6;
                color: #212529;
            }
            
            /* Content styles */
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
            
            /* Index page specific styles */
            .sidebar {
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                height: fit-content;
                position: sticky;
                top: 20px;
            }
            
            .sidebar .week-links {
                list-style-type: none;
                padding: 0;
                margin: 0;
            }
            
            .sidebar .week-links li {
                margin: 8px 0;
            }
            
            .sidebar .week-links a {
                display: block;
                padding: 8px 12px;
                background-color: #f8f9fa;
                border-radius: 4px;
                color: #495057;
                text-decoration: none;
                transition: all 0.2s ease;
            }
            
            .sidebar .week-links a:hover {
                background-color: #e9ecef;
                color: #212529;
            }
            
            .main-content {
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .readme-content {
                max-width: 100%;
                overflow-x: auto;
            }
            
            .readme-content h1 {
                font-size: 2em;
                margin-top: 0;
            }
            
            .readme-content h2 {
                font-size: 1.5em;
                margin-top: 25px;
                padding-bottom: 8px;
                border-bottom: 1px solid #eee;
            }
            
            .readme-content h3 {
                font-size: 1.2em;
                margin-top: 20px;
            }
            
            .readme-content p {
                margin: 15px 0;
            }
            
            .readme-content ul, 
            .readme-content ol {
                padding-left: 25px;
                margin: 15px 0;
            }
            
            .readme-content li {
                margin: 5px 0;
            }
            
            .readme-content code {
                background-color: #f6f8fa;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: monospace;
            }
            
            .readme-content pre {
                background-color: #f6f8fa;
                padding: 16px;
                border-radius: 6px;
                overflow-x: auto;
            }
            
            .readme-content blockquote {
                margin: 15px 0;
                padding: 0 15px;
                border-left: 4px solid #ddd;
                color: #666;
            }
            
            .readme-content table {
                border-collapse: collapse;
                width: 100%;
                margin: 15px 0;
            }
            
            .readme-content th, 
            .readme-content td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            
            .readme-content th {
                background-color: #f6f8fa;
            }
        </style>
        """

    @staticmethod
    def generate_program_page(week_program: Dict, all_programs: List[Dict]) -> str:
        """Generates a complete HTML file for a week's program"""
        nav_links = HTMLTemplates._generate_navigation_links(week_program['Week'], all_programs)
        content = HTMLTemplates._generate_week_content(week_program)
        
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Powerlifting Program - Week {week_program['Week']}</title>
            {HTMLTemplates.generate_css()}
        </head>
        <body>
            <div class="container">
                <h1><a href="index.html">6-Month Powerlifting Program</a></h1>
                <div class="week-program">
                    <div class="program-navigation">
                        {nav_links}
                    </div>
                    {content}
                </div>
            </div>
        </body>
        </html>
        """

    @staticmethod
    def _generate_navigation_links(current_week: int, all_programs: List[Dict]) -> str:
        """Generates navigation links for the program pages"""
        links = ['<div class="week-links">']
        
        # Add week selector dropdown
        links.append('<select class="week-select" onchange="window.location.href=this.value">')
        for program in all_programs:
            week_num = program["Week"]
            date = program["Date"]
            selected = ' selected' if week_num == current_week else ''
            links.append(
                f'<option value="{date}-program.html"{selected}>'
                f'Week {week_num} - {date}</option>'
            )
        links.append('</select>')
        
        # Add prev/next navigation
        if current_week > 1:
            prev_program = all_programs[current_week - 2]
            links.append(
                f'<a href="{prev_program["Date"]}-program.html" class="nav-link">← Week {current_week - 1}</a>'
            )
        
        if current_week < len(all_programs):
            next_program = all_programs[current_week]
            links.append(
                f'<a href="{next_program["Date"]}-program.html" class="nav-link">Week {current_week + 1} →</a>'
            )
            
        links.append('</div>')
        return '\n'.join(links)

    @staticmethod
    def _generate_week_content(week_program: Dict) -> str:
        """Generates the HTML content for a week's program"""
        content = [
            f'''<div class="week-header">
                <h2>Week {week_program['Week']} - {week_program['Date']}</h2>
                <div class="program-meta">
                    <p><strong>Bar:</strong> {week_program['Bar Type']}</p>
                    <p><strong>Gear:</strong> {week_program['Gear']}</p>
                </div>
            </div>'''
        ]
        
        for day, workout in week_program.items():
            if day not in ['Week', 'Bar Type', 'Chains', 'Gear', 'Date']:
                content.append(f'<div class="workout-day"><h3>{day}</h3>')
                if isinstance(workout, dict):
                    for key, value in workout.items():
                        if isinstance(value, list):
                            content.append(f'<div class="workout-section"><h4>{key}:</h4><ul>')
                            for item in value:
                                if item.startswith('-'):
                                    content.append(f'<li class="sub-item">{item[2:]}</li>')
                                else:
                                    content.append(f'<li>{item}</li>')
                            content.append('</ul></div>')
                        else:
                            content.append(f'<div class="workout-section"><h4>{key}:</h4><p>{value}</p></div>')
                else:
                    content.append(f'<p>{workout}</p>')
                content.append('</div>')
        
        return '\n'.join(content)