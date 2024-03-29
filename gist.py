import requests

def update(access_token, gist_id, filename, content):
    """
    Update a specific file in a GitHub gist.

    Parameters:
    - access_token: Your GitHub personal access token.
    - gist_id: The ID of the gist you want to update. Is the last thing on the URL, when you open it.
    - filename: The name of the file in the gist to update.
    - content: The new content to push to the file.

    """
    url = f'https://api.github.com/gists/{gist_id}'

    headers = {
        'Authorization': f'token {access_token}',
        'Content-Type': 'application/json',
    }

    data = {
        'files': {
            filename: {
                'content': content
            }
        }
    }

    response = requests.patch(url, headers=headers, json=data)

    if response.status_code != 200:
        raise f'Failed to update gist <{filename}>. Status code: {response.status_code}'

    print(f'Gist <{filename}> updated successfully.')

