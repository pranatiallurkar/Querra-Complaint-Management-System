import os
import re

html_modal = '''
<div id="logoutModalOverlay" class="logout-modal-overlay">
  <div class="logout-modal">
    <h3 style="margin-bottom:12px;"><i class="fa fa-right-from-bracket" style="color:var(--accent);"></i> Logout</h3>
    <p style="margin-bottom:24px;" class="muted">Are you sure you want to logout?</p>
    <div style="display:flex;gap:12px;justify-content:center;">
      <button class="btn btn-outline" onclick="document.getElementById('logoutModalOverlay').classList.remove('active')">Cancel</button>
      <button class="btn btn-primary" onclick="confirmLogout()">Logout</button>
    </div>
  </div>
</div>
<script>
  if(document.getElementById('logoutLink')) {
    document.getElementById('logoutLink').replaceWith(document.getElementById('logoutLink').cloneNode(true));
    document.getElementById('logoutLink').addEventListener('click', (e) => {
      e.preventDefault();
      document.getElementById('logoutModalOverlay').classList.add('active');
    });
  }
  async function confirmLogout() {
    await fetch('/api/auth/logout', {method:'POST'});
    window.location.href = '/login';
  }
</script>
</body>'''

d = 'frontend/'
for f in os.listdir(d):
    if f.endswith('.html') and f != 'login.html':
        filepath = os.path.join(d, f)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        if 'confirmLogout' not in content:
            # Remove old logout listener
            content = re.sub(r"document\.getElementById\('logoutLink'\)\.addEventListener\('click',\s*async\s*\([^)]*\)\s*=>\s*\{[^}]+\}\);", '', content, flags=re.DOTALL)
            content = re.sub(r"document\.getElementById\('logoutLink'\)\.addEventListener\('click',\s*\([^)]*\)\s*=>\s*\{[^}]+\}\);", '', content, flags=re.DOTALL)
            
            content = content.replace('</body>', html_modal)
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
