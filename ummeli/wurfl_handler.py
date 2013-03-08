from devproxy.handlers.wurfl_handler.base import WurflHandler


class UmmeliWurflHandler(WurflHandler):

    def handle_device(self, request, device):
        if device.brand_name == 'Android' or device.device_os == 'Android':
            return [{
                self.header_name: 'high',
                'X-UA-brand-name': device.brand_name,
                }]

        if device.resolution_width <= 240:
            return [{
                self.header_name: 'medium',
                'X-UA-brand-name': device.brand_name,
                }]
        else:
            return [{
                self.header_name: 'high',
                'X-UA-brand-name': device.brand_name,
                }]
