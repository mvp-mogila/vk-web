from urllib.parse import parse_qsl


def app(environ, start_response):
    data = b"Hello, World!\n"
    print(environ['wsgi.input'])

    if environ['REQUEST_METHOD'] == 'POST':
        print('POST:')
        print('Request Body:')
        print((environ['wsgi.input'].read()))


    if environ['REQUEST_METHOD'] == 'GET':
        print('GET:')
        print('Query String:')
        if environ['QUERY_STRING'] != '':
            query_str = parse_qsl(environ['QUERY_STRING'])
            for pair in query_str:
                print(f'{pair[0]} = {pair[1]}')
        else:
            print('empty')

    start_response("200 OK", [("Content-Type", "text/plain"),("Content-Length", str(len(data)))])
    return iter([data])

# ! gunicorn -w 2 -b 127.0.0.1:8081 test_wsgi:app

# * GET
# curl -G "http://127.0.0.1:8081?param1=value&param2=12345" 

# * POST
# curl -H "Content-Type: application/json" -d '{"param1": value, "param2": 12345}' "http://127.0.0.1:8081"