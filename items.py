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
        ],
    },
}


downloads = {
    '/usr/local/bin/gitea': {
        'url': 'https://dl.gitea.io/gitea/{ver}/gitea-{ver}-linux-amd64'.format(
            ver=node.metadata.get('gitea', {}).get('version', '1.8.1')),
        'sha256': node.metadata.get('gitea', {}).get('sha256',
                                                     'cc985b7947cdd50cb47a68bbb51e3a8519d0d2710a9696255928ae9912dca598'
                                                     ),
        'preceded_by': [
            'action:stop_gitea',
        ]
    },
}

actions = {
    'stop_gitea': {
        'command': 'systemctl stop gitea',
        'unless': '[ "`systemctl is-active gitea`" != "active" ]',
        'triggered': True,
        'cascade_skip': False,
    },
    'chown_gitea': {
        'command': 'chown {}:{} /usr/local/bin/gitea'.format(user, group),
        'needs': [
            'user:{}'.format(user),
            'download:/usr/local/bin/gitea',
        ],
        'needed_by': [
            'svc_systemd:gitea',
        ],
    },
    'chmod_gitea': {
        'command': 'chmod 0764 /usr/local/bin/gitea',
        'needs': [
            'download:/usr/local/bin/gitea',
        ],
        'needed_by': [
            'svc_systemd:gitea',
        ]
    }
}

directories = {
    '/var/lib/gitea/custom': {
        'owner': user,
        'group': group,
        'owner': user,
    },
    '/var/lib/gitea/data': {
        'owner': user,
        'group': group,
        'mode': '0750',
    },
    '/var/lib/gitea/indexers': {
        'owner': user,
        'group': group,
        'mode': '0750',
    },
    '/var/lib/gitea/public': {
        'owner': user,
        'group': group,
    },
    '/var/lib/gitea/log': {
        'owner': user,
        'group': group,
        'mode': '0750',
    },
    '/etc/gitea': {
        'owner': 'root',
        'group': group,
        'mode': '0750',
        'needs': [
            'user:{}'.format(user),
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
        'unless': 'test -f /etc/gitea/app.ini', # Gitea write INTERNAL_TOKEN to ini file
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
