import requests
from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')

def get_commits(request):
    username = request.GET.get('username')
    repo = request.GET.get('repo')
    branch = request.GET.get('branch', 'main')
    since = request.GET.get('since')
    until = request.GET.get('until')

    if not username or not repo:
        return JsonResponse({'error': 'Username and repo are required', 'commits': []})

    url = f"https://api.github.com/repos/{username}/{repo}/commits?sha={branch}"
    if since:
        url += f"&since={since}T00:00:00Z"
    if until:
        url += f"&until={until}T23:59:59Z"

    response = requests.get(url)
    if response.status_code != 200:
        return JsonResponse({'error': 'Failed to fetch commits', 'commits': []})

    commits = []
    for commit in response.json():
        sha = commit.get('sha')
        detail_url = f"https://api.github.com/repos/{username}/{repo}/commits/{sha}"
        detail_response = requests.get(detail_url)
        files = ['Could not fetch files'] if detail_response.status_code != 200 else [
            f['filename'] for f in detail_response.json().get('files', [])
        ]

        commits.append({
            'message': commit['commit']['message'],
            'author': commit['commit']['author']['name'] if commit['commit']['author'] else 'Unknown',
            'date': commit['commit']['author']['date'][:10] if commit['commit']['author'] else '',
            'avatar_url': commit['author']['avatar_url'] if commit.get('author') and commit['author'] else '',
            'files': files,
        })

    return JsonResponse({'commits': commits})
def get_commits_api(request):
    username = request.GET.get("username")
    repo = request.GET.get("repo")
    branch = request.GET.get("branch", "main")

    if not username or not repo:
        return JsonResponse({"error": "Missing parameters"}, status=400)

    url = f"https://api.github.com/repos/{username}/{repo}/commits?sha={branch}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        # "Authorization": "token YOUR_GITHUB_TOKEN"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return JsonResponse(response.json(), safe=False)
    else:
        return JsonResponse({"error": "Failed to fetch commits", "status_code": response.status_code}, status=500)