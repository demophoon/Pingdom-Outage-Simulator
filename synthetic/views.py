import random
import time
from pyramid.view import view_config

test_type = {}


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    global test_type
    if request.POST.get("error_type"):
        if request.GET.get("sev") not in test_type:
            test_type[request.GET.get("sev")] = 0
        test_type[request.GET.get("sev")] = int(request.POST["error_type"])
    return {"test": test_type}

XML_STRING = """
<?xml version=\"1.0\" encoding=\"UTF-8\"?>

<pingdom_http_custom_check>
    <status>%(status)s</status>
    <response_time>%(response)s</response_time>
</pingdom_http_custom_check>
"""


@view_config(route_name='test_page', renderer='string')
def test_page(request):
    current_test = test_type[request.GET.get("sev")]
    if current_test == 0:
        request.response.status = 200
        return (XML_STRING % {
            "status": "OK",
            "response": "%fms" % ((random.random() * 300) / 10.0)
        }).strip()
    elif current_test == 1:
        request.response.status = 200
        return (XML_STRING % {
            "status": "DOWN",
            "response": "%fms" % ((random.random() * 300) / 10.0)
        }).strip()
    elif current_test == 2:
        request.response.status = 200
        return ""
    elif current_test == 3:
        request.response.status = 401
        return ""
    elif current_test == 4:
        request.response.status = 500
        return ""
    elif current_test == 5:
        request.response.status = 503
        return ""
    elif current_test in range(6,18):
        request.response.status = 200
        sleep_time = ((current_test - 6) % 4 + 1) * 15
        if current_test in range(6,10):
            ret_str = (XML_STRING % {
                "status": "OK",
                "response": "%fms" % ((random.random() * 300) / 10.0 + sleep_time)
            }).strip()
        elif current_test in range(10,14):
            ret_str = (XML_STRING % {
                "status": "DOWN",
                "response": "%fms" % ((random.random() * 300) / 10.0 + sleep_time)
            }).strip()
        else:
            ret_str = ""
        time.sleep(sleep_time)
        return ret_str
    return "Nothing has been selected"
