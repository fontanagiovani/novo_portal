# coding: utf-8
from django import template
from django.template import Context, Template, Node
from portal.core.models import Menu


TEMPLATE = """
{% load mptt_tags %}
<ul>
    {% recursetree menus %}
        <li {% if node.get_leafnodes %}class="has-dropdown"{% endif %}>
            <a href="{{ node.url }}">{{ node.titulo }}</a>
            {% if not node.is_leaf_node %}
                <ul class="dropdown">
                    {{ children }}
                </ul>
            {% endif %}
        </li>
    {% endrecursetree %}
</ul>
"""


def do_menu(parser, token):
    return MenuNode()


class MenuNode(Node):
    def render(self, context):
        menus = Menu.objects.all()

        t = Template(TEMPLATE)
        c = Context({'menus': menus})
        return t.render(c)


register = template.Library()
register.tag('menu', do_menu)
