import base64
with open('karebicak.glb', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')
with open('demo-3d-card.html', 'r', encoding='utf-8') as f:
    html = f.read()
html = html.replace('src="./karebicak.glb"', f'src="data:model/gltf-binary;base64,{b64}"')
with open('demo-3d-card.html', 'w', encoding='utf-8') as f:
    f.write(html)
