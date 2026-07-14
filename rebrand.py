import os

d = 'frontend/'
for f in os.listdir(d):
    if f.endswith('.html'):
        filepath = os.path.join(d, f)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Replacements
        content = content.replace('ComplainX', 'Querra')
        content = content.replace('<div class="logo">CX</div>', '<div class="logo">Q</div>')
        
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        print('Branded', f)
