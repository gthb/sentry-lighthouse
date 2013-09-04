# coding=utf-8
"""Rudimentary plugin to create Lighthouse issues for Sentry message groups."""
from django.core.cache import cache
from lighthouse import Lighthouse as LighthouseClient
from sentry.plugins.bases.issue import IssuePlugin

from sentry_lighthouse import VERSION as PLUGINVERSION
from sentry_lighthouse.forms import LighthouseOptionsForm, LighthouseIssueForm


class LighthousePlugin(IssuePlugin):
    author = u"Gunnlaugur Þór Briem"
    author_url = "https://github.com/gthb/sentry-lighthouse"
    version = PLUGINVERSION

    slug = "lighthouse"
    title = "Lighthouse"
    conf_title = title
    conf_key = slug
    project_conf_form = LighthouseOptionsForm
    project_conf_template = "sentry_lighthouse/project_conf_form.html"
    new_issue_form = LighthouseIssueForm
    create_issue_template = 'sentry_lighthouse/create_lighthouse_issue.html'

    resource_links = [
        ("README", author_url + "/blob/master/README.rst"),
        ("Bug Tracker", author_url + "/issues"),
        ("Source", author_url),
    ]

    def is_configured(self, request, project, **kwargs):
        return bool(self.get_option('default_project', project))

    def get_lighthouse_client(self, project):
        cache_key = "sentry_lighthouse_%s" % project.pk
        client = cache.get(cache_key)
        if not client:
            instance_url = self.get_option('instance_url', project)
            token = self.get_option('token', project)
            client = LighthouseClient(token, instance_url)
            cache.set(cache_key, client)
        return client

    def get_initial_form_data(self, request, group, event, **kwargs):
        initial = {
            'title': self._get_group_title(request, group, event),
            'description': self._get_group_description(request, group, event),
            'project_id': self.get_option('default_project', group.project),
            'lighthouse_client': self.get_lighthouse_client(group.project)
        }
        return initial

    def get_new_issue_title(self):
        return "Create Lighthouse Issue"

    def create_issue(self, request, group, form_data, **kwargs):
        lighthouse_client = self.get_lighthouse_client(group.project)
        ticket = lighthouse_client.add_ticket(*(
            form_data[key]
            for key in ('project_id', 'title', 'description')
        ))
        return '%s/%s' % (ticket.project_id, ticket.number)

    def get_issue_url(self, group, issue_id, **kwargs):
        instance = self.get_option('instance_url', group.project)
        project_id, ticket_id = issue_id.split('/')
        return "%s/projects/%s/tickets/%s" % (instance, project_id, ticket_id)

    def get_issue_label(self, group, issue_id, **kwargs):
        project_id, ticket_id = issue_id.split('/')
        return "Lighthouse ticket #%s" % ticket_id
