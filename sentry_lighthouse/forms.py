import logging
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms
from lighthouse import Lighthouse as LighthouseClient

log = logging.getLogger(__name__)


class LighthouseOptionsForm(forms.Form):

    instance_url = forms.CharField(
        label=_("Lighthouse Instance URL"),
        widget=forms.TextInput(attrs={
            'class': 'span6',
            'placeholder': 'e.g. "https://mycompany.lighthouseapp.com"'
        }),
        help_text=_("The Lighthouse instance must be visible to the Sentry server"),
        required=True
    )
    token = forms.CharField(
        label=_("API Token"),
        widget=forms.TextInput(attrs={'class': 'span6'}),
        help_text=_("Lighthouse API token, from https://mycompany.lighthouseapp.com/users/12345"),
        required=True
    )
    default_project = forms.ChoiceField(
        label=_("Linked Project"),
    )

    def __init__(self, *args, **kwargs):
        super(LighthouseOptionsForm, self).__init__(*args, **kwargs)

        initial = kwargs.get("initial")
        project_safe = False
        if initial:
            # make a connection to Lighthouse to fetch a default project.
            lighthouse = LighthouseClient(
                initial.get("token"),
                initial.get("instance_url"),
            )
            projects = lighthouse.get_projects()
            if projects:
                project_choices = [
                    (p.id, "%s (%s)" % (p.name, p.id))
                    for p in projects
                ]
                project_safe = True
                self.fields["default_project"].choices = project_choices

        if not project_safe:
            del self.fields["default_project"]

    def clean_instance_url(self):
        """
        Strip forward slashes off any url passed through the form.
        """
        url = self.cleaned_data.get("instance_url")
        if url and url[-1:] == "/":
            return url[:-1]
        else:
            return url

    def clean(self):
        """
        try and build a LighthouseClient and make a random call to make sure the
        configuration is right.
        """
        cd = self.cleaned_data

        missing_fields = False
        if not cd.get("instance_url"):
            self.errors["instance_url"] = ["Instance URL is required"]
            missing_fields = True
        if not cd.get("token"):
            self.errors["token"] = ["API Token is required"]
            missing_fields = True
        if missing_fields:
            raise ValidationError("Missing Fields")

        lighthouse = LighthouseClient(cd["token"], cd["instance_url"])
        try:
            projects = lighthouse.projects
        except StandardError, se:
            self.errors["token"] = ["Failed to talk to Lighthouse; API token might be incorrect"]
            raise ValidationError("Unable to connect to Lighthouse: %s" % se)
        else:
            if not projects:
                raise ValidationError("No projects found; is API token correct?")

        return cd

# A list of common builtin custom field types for Lighthouse for easy reference.
CUSTOM_FIELD_TYPES = {
    "select": "com.atlassian.lighthouse.plugin.system.customfieldtypes:select",
    "textarea": "com.atlassian.lighthouse.plugin.system.customfieldtypes:textarea",
    "multiuserpicker": "com.atlassian.lighthouse.plugin.system.customfieldtypes:multiuserpicker"
}


class LighthouseIssueForm(forms.Form):

    project_id = forms.CharField(widget=forms.HiddenInput())

    title = forms.CharField(
        label=_("Issue Summary"),
        widget=forms.TextInput(attrs={'class': 'span6'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": 'span6'})
    )

    def __init__(self, *args, **kwargs):
        initial = kwargs.get("initial")
        lighthouse_client = initial.pop("lighthouse_client")

        # Returns the metadata the configured Lighthouse instance requires for
        # creating issues for a given project.
        project_id = initial.get("project_id")
        project = lighthouse_client.get_project(project_id)

        # set back after we've played with the inital data
        kwargs["initial"] = initial

        # call the super to bind self.fields from the defaults.
        super(LighthouseIssueForm, self).__init__(*args, **kwargs)

        self.fields["project_id"].initial = project.id

    def clean_description(self):
        """
        Turn code blocks that are in the stack trace into Lighthouse code blocks.
        """
        desc = self.cleaned_data["description"]
        return desc.replace("```", "@@@")
