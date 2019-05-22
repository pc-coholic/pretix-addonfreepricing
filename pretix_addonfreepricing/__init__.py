from django.utils.translation import ugettext_lazy

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")


class PluginApp(PluginConfig):
    name = 'pretix_addonfreepricing'
    verbose_name = 'Free pricing for AddOns'

    class PretixPluginMeta:
        name = ugettext_lazy('Free pricing for AddOns')
        author = 'Martin Gross'
        description = ugettext_lazy('This plugin allows you to offer free price input for AddOns')
        visible = True
        version = '1.0.0'
        compatibility = "pretix>=2.7.0"

    def ready(self):
        from . import signals  # NOQA


default_app_config = 'pretix_addonfreepricing.PluginApp'
