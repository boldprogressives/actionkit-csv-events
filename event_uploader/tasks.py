from actionkit import Client as XMLRPCClient
from celery.decorators import task

@task()
def create_actionkit_event(struct):
    actionkit = XMLRPCClient()
    return actionkit.Event.create(struct)
