import re

def process_blog_html():
    filepath = 'blog.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The cards currently start with:
    # <a href="blog/..." class="group max-w-[450px] mx-auto w-full bg-white border border-gray-100 rounded-2xl overflow-hidden shadow-soft hover:shadow-elegant hover:-translate-y-1 transition flex flex-col">
    # We want to change the <a> class to remove bg-white, border, border-gray-100, overflow-hidden and add card-sweep.
    # And we want to wrap the inner content in:
    # <div class="relative z-10 flex flex-col h-full w-full bg-white rounded-[inherit] overflow-hidden border border-gray-100">

    def replace_card(match):
        href = match.group(1)
        inner_content = match.group(2)
        
        # New <a> tag
        new_a = f'<a href="{href}" class="group max-w-[450px] mx-auto w-full rounded-2xl shadow-soft hover:shadow-elegant hover:-translate-y-1 transition flex flex-col card-sweep">'
        
        # New inner wrapper
        new_inner = f'\n      <div class="relative z-10 flex flex-col h-full w-full bg-white rounded-[inherit] overflow-hidden border border-gray-100">\n{inner_content}\n      </div>\n    </a>'
        
        return new_a + new_inner

    # Regex to match the whole card block
    # Note: Using a non-greedy match .*? to capture everything inside the <a>...</a>
    pattern = r'<a href="(blog/[^"]+)" class="group max-w-\[450px\] mx-auto w-full bg-white border border-gray-100 rounded-2xl overflow-hidden shadow-soft hover:shadow-elegant hover:-translate-y-1 transition flex flex-col">(.*?)</a>'
    
    new_content, count = re.subn(pattern, replace_card, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {count} cards in blog.html")
    else:
        print("No cards matched the pattern in blog.html")

if __name__ == '__main__':
    process_blog_html()
