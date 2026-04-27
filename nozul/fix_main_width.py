import os
import re

for root, dirs, files in os.walk('.'):
    if 'assets' in root or '.git' in root or '.gemini' in root or 'components' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Use regex to find <main>...</main> and replace max-w-[1650px] inside it
            def replace_main(match):
                main_content = match.group(0)
                # Change 1650px to 1440px (a standard middle-ground width)
                # We can also change max-w-7xl if it's there, but we already reverted to 1650px.
                return main_content.replace('max-w-[1650px]', 'max-w-[1440px]')
                
            new_content = re.sub(r'<main>.*?</main>', replace_main, content, flags=re.DOTALL)
            
            # Some sections might not be inside <main>. For example, older files might just have <section>.
            # But let's check if new_content is different. If not, it means either no main tag, or no 1650px in main.
            # Wait, in index.html, is there a <main> tag? Let's check visually or just do it.
            # To be safe, let's just replace all max-w-[1650px] EXCEPT those inside <header> and <footer>.
            
            # Better approach: 
            # 1. find all indices of max-w-[1650px]
            # 2. check if they fall inside <header>...</header> or <footer>...</footer>
            
            # But regex sub is easier. We temporarily hide header and footer.
            header_pattern = r'<header.*?</header>'
            footer_pattern = r'<footer.*?</footer>'
            
            headers = []
            footers = []
            
            def save_header(m):
                headers.append(m.group(0))
                return f"__HEADER_{len(headers)-1}__"
                
            def save_footer(m):
                footers.append(m.group(0))
                return f"__FOOTER_{len(footers)-1}__"
                
            temp_content = re.sub(header_pattern, save_header, content, flags=re.DOTALL)
            temp_content = re.sub(footer_pattern, save_footer, temp_content, flags=re.DOTALL)
            
            # Now replace max-w-[1650px] with max-w-[1400px] in the remaining content
            temp_content = temp_content.replace('max-w-[1650px]', 'max-w-[1400px]')
            
            # Restore headers and footers
            for i, h in enumerate(headers):
                temp_content = temp_content.replace(f"__HEADER_{i}__", h)
            for i, f in enumerate(footers):
                temp_content = temp_content.replace(f"__FOOTER_{i}__", f)
                
            if temp_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(temp_content)
                print(f"Updated main width in {filepath}")
