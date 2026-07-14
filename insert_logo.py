import os

d = 'frontend/'
for f in os.listdir(d):
    if f.endswith('.html'):
        filepath = os.path.join(d, f)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Replace the sidebar logo
        content = content.replace('<div class="logo">Q</div>', '<img src="/assets/logo.png" alt="Querra Logo" class="brand-logo">')
        
        # Replace the login page hero logo
        if f == 'login.html':
            import re
            content = re.sub(r'<h1 style="font-size: 3\.5rem; font-weight: 800; margin-bottom: 8px; letter-spacing: 2px;">\s*<i class="fa fa-bolt" style="color:var\(--accent\);margin-right:12px;"></i><span class="text-gradient">Querra</span>\s*</h1>',
                             '<div style="margin-bottom: 24px;"><img src="/assets/logo.png" alt="Querra Logo" style="height: 140px; width: auto; object-fit: contain;"></div>', content)
            
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        print('Updated logo in', f)
