import os
import re

d = 'frontend/'
for f in os.listdir(d):
    if f.endswith('.html') and f != 'login.html':
        filepath = os.path.join(d, f)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Regex to match the broken leftover script part
        # <script>
        #   window.location.href='/login';
        # });
        fixed_content = re.sub(r'<script>\s*window\.location\.href\s*=\s*[\'"]/login[\'"];\s*\}\);', '<script>', content)
        
        if fixed_content != content:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(fixed_content)
            print('Fixed', f)
