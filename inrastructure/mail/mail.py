from jinja2 import Environment, FileSystemLoader



def render_template(template_root: str, template_name: str, data: dict) -> str:
    environment = Environment(loader=FileSystemLoader(template_root))
    template = environment.get_template(template_name)
    return template.render(data)