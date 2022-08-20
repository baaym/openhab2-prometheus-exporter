import urllib.request
import json
import time

def get_item_type(item):
   return item['type'].lower().split(':')[0]

def get_metrics():
    url = urllib.request.urlopen('http://127.0.0.1:8080/rest/items?recursive=false&fields=name,state,type')
    content_bytes = url.read()
    content = content_bytes.decode('utf-8')

    url.close()

    obj = json.loads(content)
    ts = int(round(time.time() * 1000))

    numbers = [ item for item in obj if get_item_type(item) == 'number' ]
    dimmers = [ item for item in obj if get_item_type(item) == 'dimmer' ]
    switches = [ item for item in obj if get_item_type(item) == 'switch' ]
    contacts = [ item for item in obj if get_item_type(item) == 'contact' ]

    res = ''
    res = res + print_metrics(numbers, 'number', ts)
    res = res + print_metrics(dimmers, 'dimmer', ts)
    res = res + print_metrics(switches, 'switch', ts)
    res = res + print_metrics(contacts, 'contact', ts)

    return res


def print_metrics(metrics, type, timestamp):
    metric_name = 'openhab2_metric_' + type

    res = '# TYPE {} gauge\n'.format(metric_name)

    for metric in metrics:
        name = metric['name']
        value = metric['state'].split(' ')[0]

        if value is None or value == 'NULL':
            continue

        if metric['type'].lower() == 'switch':
            value = 1 if value == 'ON' else 0
        elif metric['type'].lower() == 'contact':
            value = 1 if value == 'OPEN' else 0

        res = res + metric_name + '{name="' + name + '"} ' + '{} {}\n'.format(value, timestamp)

    return res


def app(environ, start_response):
    """
    Entrypoint for gunicorn
    """
    metrics = get_metrics()
    data = metrics.encode('utf-8')

    start_response('200 OK', [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(data)))
        ])

    return iter([data])
