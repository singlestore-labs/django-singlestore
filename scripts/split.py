#!/usr/bin/env python3
"""
Script to split setup.sql into separate files based on comment sections.
Each section will be saved as {section_name}_setup.sql
"""

import os
import re

def split_sql_file(input_file, output_dir):
    """Split the SQL file into sections based on comments."""
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Split content by comment lines that start with "-- "
    sections = []
    current_section = None
    current_content = []
    
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        # Check if this is a section comment (starts with "-- " followed by word characters)
        if re.match(r'^-- \w+', line.strip()):
            # Save previous section if it exists
            if current_section and current_content:
                # Remove empty lines from the beginning and end
                while current_content and not current_content[0].strip():
                    current_content.pop(0)
                while current_content and not current_content[-1].strip():
                    current_content.pop()
                
                if current_content:  # Only add if there's actual content
                    sections.append((current_section, '\n'.join(current_content)))
            
            # Start new section
            current_section = line.strip()[3:]  # Remove "-- " prefix
            current_content = [line]
            print(f"Found section: {current_section} at line {i+1}")
        else:
            # Add line to current section
            if current_section is not None:
                current_content.append(line)
    
    # Don't forget the last section
    if current_section and current_content:
        while current_content and not current_content[0].strip():
            current_content.pop(0)
        while current_content and not current_content[-1].strip():
            current_content.pop()
        if current_content:
            sections.append((current_section, '\n'.join(current_content)))
    
    # Write each section to its own file
    for section_name, section_content in sections:
        # Clean up section name for filename
        filename = f"{section_name}_setup.sql"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(section_content)
            f.write('\n')  # Ensure file ends with newline
        
        print(f"Created: {filepath}")
    
    print(f"\nTotal sections created: {len(sections)}")

if __name__ == "__main__":
    input_file = "/home/parth/workplace/django-singlestore/scripts/setup.sql"
    output_dir = "/home/parth/workplace/django-singlestore/scripts/setup_sections"
    
    split_sql_file(input_file, output_dir)