import os

root_dir = r'c:\Users\Serdarowski\Desktop\verisyon 2'

def update_footer_padding(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    c = f.read()
                
                # Footer padding'i daralt (py-16 -> py-10)
                if 'py-16 grid gap-10 md:grid-cols-2 lg:grid-cols-4' in c:
                    c = c.replace('py-16 grid gap-10 md:grid-cols-2 lg:grid-cols-4', 'py-10 grid gap-10 md:grid-cols-2 lg:grid-cols-4')
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(c)
                    print(f"Updated footer padding in: {file}")

update_footer_padding(root_dir)
