import os
import re
import urllib.request
import urllib.error

def get_depth(filepath):
    # Calculate depth relative to root
    parts = os.path.relpath(filepath, '.').split(os.sep)
    if len(parts) == 1:
        return ''
    return '../' * (len(parts) - 1)

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

ensure_dir('assets/images')
ensure_dir('assets/css')
ensure_dir('assets/js')

# Create the standard CSS and JS files
css_content = """html{scroll-behavior:smooth; overflow-y: scroll;}
body{font-family:'Inter',sans-serif;-webkit-font-smoothing:antialiased}
.font-display{font-family:'Space Grotesk',sans-serif}
.bg-grid{background-image:radial-gradient(rgba(255,255,255,.07) 1px,transparent 1px);background-size:32px 32px}
.text-gradient{background:linear-gradient(135deg,#ff7a2d,#ffb380);-webkit-background-clip:text;background-clip:text;color:transparent}
.fade-in{opacity:0;transform:translateY(12px);animation:fi .7s forwards}
@keyframes fi{to{opacity:1;transform:none}}
@keyframes marquee {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
.animate-marquee {
  display: flex;
  width: max-content;
  animation: marquee 40s linear infinite;
}
.animate-marquee:hover {
  animation-play-state: paused;
}
details>summary{list-style:none;cursor:pointer}
details>summary::-webkit-details-marker{display:none}
.prose-custom h2{font-family:'Space Grotesk',sans-serif;font-size:1.5rem;font-weight:700;margin-top:1.75rem;margin-bottom:.6rem;color:#0f1115}
.prose-custom p{margin:0 0 1rem;line-height:1.75;color:#374151}
.prose-custom ul{margin:0 0 1rem 1.25rem;list-style:disc}
.prose-custom li{margin:.25rem 0;color:#374151}
.prose-custom strong{color:#0f1115}
"""
with open('assets/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

js_tailwind = """tailwind.config = {
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT:'#ff7a2d', 600:'#f06b1c', 50:'#fff3eb' },
        ink: '#0f1115',
        surface: '#f7f7f8',
      },
      fontFamily: {
        sans: ['Inter','ui-sans-serif','system-ui','sans-serif'],
        display: ['"Space Grotesk"','ui-sans-serif','system-ui','sans-serif'],
      },
      boxShadow: {
        soft: '0 6px 20px -10px rgba(15,17,21,0.18)',
        elegant: '0 24px 48px -16px rgba(255,122,45,0.35)',
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(135deg,#ff7a2d 0%,#ff9a55 100%)',
        'gradient-hero': 'linear-gradient(135deg,#0f1115 0%,#1a1d24 60%,#262932 100%)',
      },
    }
  }
}"""
with open('assets/js/tailwind-config.js', 'w', encoding='utf-8') as f:
    f.write(js_tailwind)

js_main = """document.addEventListener('DOMContentLoaded', () => {
  const mnav = document.getElementById('mnav');
  const mmenu = document.getElementById('mmenu');
  if (mnav && mmenu) {
    mnav.addEventListener('click', () => {
      mmenu.classList.toggle('hidden');
    });
  }
});
"""
with open('assets/js/main.js', 'w', encoding='utf-8') as f:
    f.write(js_main)

# Regex to find wp-content images
img_pattern = re.compile(r'src="(https?://www\.nozulmakina\.com\.tr/wp-content/uploads/[^"]+)"')

for root, dirs, files in os.walk('.'):
    if 'assets' in root or '.git' in root or '.gemini' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            depth = get_depth(filepath)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Process images
            urls = img_pattern.findall(content)
            for url in urls:
                filename = url.split('/')[-1]
                
                # Try to get higher quality by removing dimension suffixes like -500x540
                hq_filename = re.sub(r'-\d+x\d+(?=\.[a-zA-Z]+$)', '', filename)
                hq_url = url.replace(filename, hq_filename)
                
                local_path = os.path.join('assets/images', hq_filename)
                
                if not os.path.exists(local_path):
                    print(f"Downloading {hq_url}")
                    try:
                        urllib.request.urlretrieve(hq_url, local_path)
                        filename_to_use = hq_filename
                    except Exception as e:
                        print(f"Failed to download HQ, falling back to original: {url}")
                        local_path = os.path.join('assets/images', filename)
                        try:
                            urllib.request.urlretrieve(url, local_path)
                            filename_to_use = filename
                        except Exception as e2:
                            print(f"Failed to download original too: {e2}")
                            filename_to_use = filename # keep it as is, maybe broken link
                else:
                    filename_to_use = hq_filename
                    
                # Replace in content
                content = content.replace(url, f'{depth}assets/images/{filename_to_use}')
            
            # Remove inline styles
            content = re.sub(r'<style>.*?</style>', f'<link rel="stylesheet" href="{depth}assets/css/style.css" />', content, flags=re.DOTALL)
            
            # Replace tailwind config script
            content = re.sub(r'<script>\s*tailwind\.config\s*=.*?</script>', f'<script src="{depth}assets/js/tailwind-config.js"></script>', content, flags=re.DOTALL)
            
            # Remove anti-copy scripts
            anti_copy_pattern = r'<script>\s*document\.addEventListener\(\'contextmenu\'.*?</script>'
            content = re.sub(anti_copy_pattern, f'<script src="{depth}assets/js/main.js"></script>', content, flags=re.DOTALL)
            
            # If the file didn't have the anti copy script, just append main.js before </body>
            if f'{depth}assets/js/main.js' not in content:
                content = content.replace('</body>', f'<script src="{depth}assets/js/main.js"></script>\n</body>')
                
            # Remove inline mobile menu script
            content = re.sub(r'<script>document\.getElementById\(\'mnav\'\).*?</script>', '', content)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

print("Done processing files.")
