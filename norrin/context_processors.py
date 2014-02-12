from norrin import config

def norrin_config(request):
    return {
        'config': {
            'notifications_enabled': config.get(config.SERVICES_ENABLED, 'off'),
        }
    }
