import warnings

from django import template
from django.utils.html import mark_safe

from feincms3.templatetags.feincms3 import render_region


warnings.warn(
    "Load render_region using {% load feincms3 %} instead."
    " The feincms3_renderer template tag library and the render_plugin and"
    " render_plugins tags have been deprecated and will be removed soon.",
    Warning,
)


register = template.Library()
register.simple_tag(takes_context=True)(render_region)


@register.simple_tag(takes_context=True)
def render_plugin(context, plugin):
    """
    Render a single plugin. Requires the
    :class:`feincms3.renderer.TemplatePluginRenderer` instance in the context
    as ``renderer``::

        {% render_plugin plugin %}

    In general you should prefer
    :func:`~feincms3.templatetags.feincms3.render_region` over this
    tag.
    """
    return context["renderer"].render_plugin_in_context(plugin, context)


@register.simple_tag(takes_context=True)
def render_plugins(context, plugins):
    """
    Render a list of plugins. Requires the
    :class:`feincms3.renderer.TemplatePluginRenderer` instance in the context
    as ``renderer``::

        {% render_plugins plugins %}

    This plugin is equivalent to::

        {% for plugin in plugins %}{% render_plugin plugin %}{% endfor %}

    In general you should prefer
    :func:`~feincms3.templatetags.feincms3.render_region` over this
    tag.
    """
    renderer = context["renderer"]
    return mark_safe(
        "".join(
            renderer.render_plugin_in_context(plugin, context) for plugin in plugins
        )
    )
