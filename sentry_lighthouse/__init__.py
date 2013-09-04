try:
    VERSION = __import__('pkg_resources').get_distribution('sentry_lighthouse').version
except Exception, e:
    VERSION = "dev"
