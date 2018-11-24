mysql_db = node.metadata.get('gitea', {}).get('db', {}).get('db', 'gitea')
mysql_host = node.metadata.get('gitea', {}).get('db', {}).get('host', 'localhost')
mysql_user = node.metadata.get('db', {}).get('user', 'gitea')
mysql_password = node.metadata.get('gitea', {}).get('db', {}).\
    get('password', repo.vault.password_for("mysql_{}_user_{}".format(mysql_user, node.name)))

user = node.metadata.get('gitea', {}).get('user', 'gitea')
group = node.metadata.get('gitea', {}).get('group', 'gitea')

if mysql_host == 'localhost':
    mysql_users = {
        mysql_user: {
            'password': mysql_password,
            'hosts': ['127.0.0.1', '::1', 'localhost'].copy(),
            'db_priv': {
                mysql_db: 'all',
            },
        }
    }

    mysql_dbs = {
        mysql_db: {
        }
    }

svc_systemd = {
    'gitea': {
        'enabled': True,
        'needs': [
            'download:/usr/local/bin/gitea',
            'file:/etc/gitea/app.ini',
            'action:create_gitea_user',
        ],
    },
}

downloads = {
    '/usr/local/bin/gitea': {
        'url': 'https://dl.gitea.io/gitea/{ver}/gitea-{ver}-linux-amd64' \
            .format(ver=node.metadata.get('gitea', {}).get('version', '1.4')),
        'sha256': node.metadata.get('gitea', {}).get('sha256', \
            '9e4d558c937abe3d16ab57520aaecdd003345fbfc72bb3f52dabe9be739fdad5'),
    },
}

actions = {
    'create_gitea_user': {
        'command': 'useradd -c "Gitea User" -d /var/lib/gitea -m -s /bin/bash {}'.format(user),
        'unless': 'id -u {}'.format(user),
    },
    'chown_gitea': {
        'command': 'chown {}:{} /usr/local/bin/gitea'.format(user, group),
        'needs': [
            'action:create_gitea_user',
            'download:/usr/local/bin/gitea',
        ],
        'needed_by': [
            'svc_systemd:gitea',
        ],
    },
    'chmod_gitea': {
        'command': 'chmod 0764 /usr/local/bin/gitea',
        'needs': [
            'action:create_gitea_user',
            'download:/usr/local/bin/gitea',
        ],
        'needed_by': [
            'svc_systemd:gitea',
        ]
    }
}

directories = {
    '/var/lib/gitea': {
        'owner': user,
        'group': group,
        'needs': [
            'action:create_gitea_user',
        ]
    },
    '/var/lib/gitea/custom': {
        'owner': user,
        'group': group,
        'owner': user,
        'needs': [
            'action:create_gitea_user',
        ]
    },
    '/var/lib/gitea/data': {
        'owner': user,
        'group': group,
        'mode': '0750',
        'needs': [
            'action:create_gitea_user',
        ]
    },
    '/var/lib/gitea/indexers': {
        'owner': user,
        'group': group,
        'mode': '0750',
        'needs': [
            'action:create_gitea_user',
        ]
    },
    '/var/lib/gitea/public': {
        'owner': user,
        'group': group,
        'needs': [
            'action:create_gitea_user',
        ]
    },
    '/var/lib/gitea/log': {
        'owner': user,
        'group': group,
        'mode': '0750',
        'needs': [
            'action:create_gitea_user',
        ]
    },
    '/etc/gitea': {
        'owner': 'root',
        'group': group,
        'mode': '0750',
        'needs': [
            'action:create_gitea_user',
        ]
    }
}

files = {
    '/etc/gitea/app.ini': {
        'source': 'etc/gitea/app.ini',
        'content_type': 'mako',
        'context': {
            'gitea': node.metadata.get('gitea', {}),
        },
        'owner': user,
        'group': group,
        'mode': '0644',
        'needs': [
            'action:create_gitea_user',
        ]
    },
    '/etc/systemd/system/gitea.service': {
        'source': 'etc/systemd/system/gitea.service',
        'content_type': 'mako',
        'context': {
            'gitea': node.metadata.get('gitea', {}),
        },
        'owner': 'root',
        'group': 'root',
        'needs': [
            'file:/etc/gitea/app.ini',
        ],
        'triggers': [
            'svc_systemd:gitea:restart',
        ]
    }
}

