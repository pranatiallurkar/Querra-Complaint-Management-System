import os
import re

d = 'frontend/'
for f in os.listdir(d):
    if f.endswith('.html'):
        filepath = os.path.join(d, f)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Undo sidebar logo
        content = content.replace('<img src="/assets/logo.png" alt="Querra Logo" class="brand-logo">', '<div class="logo">Q</div>')
        
        # Undo login page hero logo
        if f == 'login.html':
            content = content.replace(
                '<div style="margin-bottom: 24px;"><img src="/assets/logo.png" alt="Querra Logo" style="height: 140px; width: auto; object-fit: contain;"></div>',
                '<h1 style="font-size: 3.5rem; font-weight: 800; margin-bottom: 8px; letter-spacing: 2px;">\n        <i class="fa fa-bolt" style="color:var(--accent);margin-right:12px;"></i><span class="text-gradient">Querra</span>\n      </h1>'
            )
            
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        print('Reverted logo in', f)
