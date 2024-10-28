from io_handler import get_file_contents
from pathlib import Path
from nodehandlers import markdown_to_html_node, extract_title, strip_title

def generate_page(from_path:Path, template_path:Path, dest_path:Path):
    print(f"\nGenerating page from \n{from_path} \nto \n{dest_path} \nusing \n{template_path}")

    md_contents = get_file_contents(from_path)
    template = get_file_contents(template_path)
    title = extract_title(md_contents)
    
    contents = markdown_to_html_node(md_contents)

    titled_html = template.replace("{{ Title }}", title)
    full_html = titled_html.replace("{{ Content }}", contents)
    

    
    html_contents = markdown_to_html_node(full_html)
    dest_path.write_text(html_contents)
