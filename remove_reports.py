import os
import re

d = 'frontend/'
for f in os.listdir(d):
    if f.endswith('.html'):
        filepath = os.path.join(d, f)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Remove the reports navigation link, allowing for class="active" or just normal
        fixed_content = re.sub(r'<a.*?href="/admin_reports".*?>.*?Reports</a>', '', content)
        
        if fixed_content != content:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(fixed_content)
            print('Removed from', f)
