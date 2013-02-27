def get_recognised_device(request):
    device_override = request.session.get('device_override', None)
    if device_override:
        device = device_override
    else:
        device = request.META.get('HTTP_X_UA_BRAND_NAME', 'Other')

    return {
        'nokia': {
            'name': device,
            'template': 'opportunities/tomtom/qualify_device_nokia.html'
        },
        'samsung': {
            'name': device,
            'template': 'opportunities/tomtom/qualify_device_samsung.html'
        },
        'rim': {
            'name': 'BlackBerry',
            'template': 'opportunities/tomtom/qualify_device_blackberry.html'
        },
        'apple': {
            'name': device,
            'template': 'opportunities/tomtom/qualify_device_apple.html'
        },
        'motorola': {
            'name': device,
            'template': 'opportunities/tomtom/qualify_device_motorola.html'
        },
        'android': {
            'name': 'Android',
            'template': 'opportunities/tomtom/qualify_device_google.html'
        },
        'google': {
            'name': 'Android',
            'template': 'opportunities/tomtom/qualify_device_google.html'
        },
    }.get(device.lower(),
        {'name': 'Other',
        'template': 'opportunities/tomtom/qualify_device_other.html'})


def recognised_device_processor(request):
    return {'device': get_recognised_device(request)}
