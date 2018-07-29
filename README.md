# Dependencies
- MySQL-Bundle (not published yet)
- Downloads-Item: https://github.com/sHorst/bw.item.download

# Config
```
    'gitea': {
        'name': 'Gitea',
        'user': 'gitea',
        'mode': 'prod',
        'server': {
            'protocol': 'http',
            'domain': 'localhost',
            'root_url': '%(PROTOCOL)s://%(DOMAIN)s:%(HTTP_PORT)s/',
            'http_addr': '0.0.0.0',
            'http_port': '3000',
            'unix_socket_permission': '666',
        },
        'db': {
            'type': 'mysql',
            'host': 'localhost',
            'port': '3306',
            'user': 'gitea',
            'password': '[generated]',
        },
    }
```