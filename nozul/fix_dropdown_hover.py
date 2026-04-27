import os

OLD_SPAN = 'class="text-sm font-semibold text-gray-800 group-hover:text-primary transition-colors"'
NEW_SPAN = 'class="text-sm font-semibold text-gray-900 transition-colors"'

root_dir = r'C:\Users\Serdarowski\Desktop\verisyon 2'
updated = 0

for dirpath, dirnames, filenames in os.walk(root_dir):
    dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules']]
    for fname in filenames:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(dirpath, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if OLD_SPAN in content:
            new_content = content.replace(OLD_SPAN, NEW_SPAN)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  Updated: {os.path.relpath(fpath, root_dir)}")
            updated += 1

print(f"\nTotal files updated: {updated}")
