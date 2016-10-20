from dynamic_preferences.types import BooleanPreference, IntegerPreference, StringPreference, Section
from dynamic_preferences.registries import user_preferences_registry
from django import forms


email_settings = Section('email_settings')
render_settings = Section('render_settings')


@user_preferences_registry.register
class EnableTLS(BooleanPreference):
    """Do you want to be notified on comment publication ?"""
    section = email_settings
    name = 'enable_TSL'
    default = True
    verbose_name = 'Enable TLS'
    help_text = 'check, if you want to enable TLS'


@user_preferences_registry.register
class EmailHost(StringPreference):
    section = email_settings
    name = 'comment_notifications_enabled'
    default = 'smtp.gmail.com'
    verbose_name = 'E-mail host'
    help_text = 'outgoing server (e.g. smtp)'


@user_preferences_registry.register
class EmailHostUser(StringPreference):
    section = email_settings
    name = 'email_host_user'
    default = 'mail@example.com'
    verbose_name = 'Username'
    help_text = 'your email login username'


class PasswordField(forms.CharField):
    def __init__(self, *args, **kwargs):
        self.widget = forms.PasswordInput
        self.required = False
        super(PasswordField, self).__init__(*args, **kwargs)


@user_preferences_registry.register
class EmailPassword(StringPreference):
    section = email_settings
    field_class = PasswordField
    name = 'email_password'
    default = 'password'
    verbose_name = 'Password'
    help_text = 'your email login password'


@user_preferences_registry.register
class EmailPort(IntegerPreference):
    section = email_settings
    name = 'email_port'
    default = 587
    verbose_name = 'Port'
    help_text = 'email port'


@user_preferences_registry.register
class HeadSize(IntegerPreference):
    section = render_settings
    name = 'head_size'
    default = 150
    verbose_name = 'Headline Size'
    help_text = 'survey headline font size'


@user_preferences_registry.register
class DescSize(IntegerPreference):
    section = render_settings
    name = 'desc_size'
    default = 80
    verbose_name = 'Description Size'
    help_text = 'survey description font size'


@user_preferences_registry.register
class QuestionSize(IntegerPreference):
    section = render_settings
    name = 'question_size'
    default = 100
    verbose_name = 'Question Size'
    help_text = 'Question font size'


@user_preferences_registry.register
class ChoiceSize(IntegerPreference):
    section = render_settings
    name = 'choice_size'
    default = 70
    verbose_name = 'Choice Size'
    help_text = 'Choice font size'