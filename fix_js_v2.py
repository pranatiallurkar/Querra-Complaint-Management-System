import os
import re

d = 'frontend/'
for f in os.listdir(d):
    if f.endswith('.html') and f != 'login.html':
        filepath = os.path.join(d, f)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Remove the broken leftover part anywhere in the file
        fixed_content = re.sub(r'window\.location\.href\s*=\s*[\'"]/login[\'"];\s*\}\);', '', content)
        
        if fixed_content != content:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(fixed_content)
            print('Fixed', f)
