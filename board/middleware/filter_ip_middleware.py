import time
import datetime
from django.core.exceptions import PermissionDenied


class FilterIpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_ips = [
            '127.0.0.1'
        ]
        ip = request.META.get('REMOTE_ADDR')
        if ip not in allowed_ips:
            raise PermissionDenied

        response = self.get_response(request)

        return response


class IncreaseResponseTime:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tic = time.perf_counter() + 2
        new_tic = time.perf_counter()
        while new_tic < tic:
            new_tic = time.perf_counter()

        response = self.get_response(request)
        return response


class SimpleDosFilter:
    def __init__(self, get_response):
        self.get_response = get_response
        self.last_request_list = []
        self.max_sec_filter_time = 10
        self.max_request_value = 2

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        now = datetime.datetime.now()
        self.last_request_list.append((ip, now))
        min_datetime = now - datetime.timedelta(seconds=self.max_sec_filter_time)
        self.last_request_list = [ip_time for ip_time in self.last_request_list if ip_time[1] > min_datetime]
        last_request_from_ip_count = sum([1 for ip_time in self.last_request_list if ip_time[0] == ip])
        if last_request_from_ip_count > self.max_request_value:
            raise PermissionDenied

        response = self.get_response(request)
        return response
