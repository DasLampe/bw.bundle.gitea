@metadata_processor
def add_gitea_user(metadata):
    if node.has_bundle('users'):
        metadata['users'][metadata.get('gitea', {}).get('user', 'gitea')] = {
                'sudo': False,
                'full_name': 'Gitea User',
                'shell': '/bin/bash',
                'home': '/var/lib/gitea',
        }
    return metadata, DONE
