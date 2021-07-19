from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from core.pubsub_service import publisher, listener

        try:
            publisher()
            listener()
        
        except Exception as error:
            print(error)