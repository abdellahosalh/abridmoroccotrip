import os

directory = r"c:\Users\LENOVO THINKPAD\Documents\Nouveau dossier\abridmoroccotrip-main"

literal_replacements = [
    # 36 -> 47
    ("$36", "$47"),
    ('"price": "36"', '"price": "47"'),
    ('"price":"36"', '"price":"47"'),
    ("($36)", "($47)"),
    
    # 61 -> 79
    ("$61", "$79"),
    ('"price": "61"', '"price": "79"'),
    ('"price":"61"', '"price":"79"'),
    ("($61)", "($79)"),
    
    # 84 -> 109
    ("$84", "$109"),
    ('"price": "84"', '"price": "109"'),
    ('"price":"84"', '"price":"109"'),
    ("($84)", "($109)"),
    
    # 97 -> 126
    ("$97", "$126"),
    ('"price": "97"', '"price": "126"'),
    ('"price":"97"', '"price":"126"'),
    ("($97)", "($126)"),
    
    # 180 -> 234
    ("$180", "$234"),
    ('"price": "180"', '"price": "234"'),
    ('"price":"180"', '"price":"234"'),
    ("($180)", "($234)"),
    
    # 250 -> 325
    ("$250", "$325"),
    ('"price": "250"', '"price": "325"'),
    ('"price":"250"', '"price":"325"'),
    ("($250)", "($325)"),
    
    # 2,156 -> 2,803
    ("$2,156", "$2,803"),
    ('"price": "2156"', '"price": "2803"'),
    ('"price":"2156"', '"price":"2803"'),
    ("($2,156)", "($2,803)"),
    
    # 2,260 -> 2,938
    ("$2,260", "$2,938"),
    ("$2,260+", "$2,938+"),
    ('"price": "2260"', '"price": "2938"'),
    ('"price":"2260"', '"price":"2938"'),
    ("($2,260)", "($2,938)")
]

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content

    for old, new in literal_replacements:
        new_content = new_content.replace(old, new)
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {os.path.basename(filepath)}")

count = 0
for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith('.html') or file.endswith('.js') or file.endswith('.xml') or file.endswith('.css'):
            update_file(os.path.join(root, file))
            count += 1

print(f"Finished scanning {count} files and applied the +30% increase!")
