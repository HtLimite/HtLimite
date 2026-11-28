import html
import json
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

USER = os.environ.get('DASHBOARD_USER', 'HtLimite')
BASE = 'https://api.github.com'


def api(path, payload=None):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'profile-dashboard'}
    if os.environ.get('GH_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    data = None if payload is None else json.dumps(payload).encode()
    if data is not None:
        headers['Content-Type'] = 'application/json'
    with urllib.request.urlopen(urllib.request.Request(BASE + path, data=data, headers=headers), timeout=30) as response:
        return json.load(response)


def collect():
    profile = api(f'/users/{USER}')
    repos = []
    for page in range(1, 101):
        batch = api(f'/users/{USER}/repos?type=owner&per_page=100&page={page}')
        if not isinstance(batch, list):
            raise ValueError('Invalid repository response')
        repos.extend(r for r in batch if not r['private'])
        if len(batch) < 100:
            break
    else:
        raise ValueError('Repository pagination limit reached')
    languages = Counter()
    for repo in repos:
        if not repo['fork']:
            languages.update(api(f"/repos/{repo['full_name']}/languages"))
    query = '''query($login: String!) { user(login: $login) { contributionsCollection {
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    } } }'''
    result = api('/graphql', {'query': query, 'variables': {'login': USER}})
    if result.get('errors'):
        raise ValueError('Contribution GraphQL query failed')
    calendar = result['data']['user']['contributionsCollection']['contributionCalendar']
    days = sorted((date.fromisoformat(d['date']), d['contributionCount']) for w in calendar['weeks'] for d in w['contributionDays'])
    return profile, repos, languages, days, calendar['totalContributions']


def metrics(days, total, today):
    if not days or days[-1][0] not in (today, today - timedelta(days=1)):
        raise ValueError('Missing or stale contribution calendar')
    if any(not isinstance(n, int) or n < 0 for _, n in days):
        raise ValueError('Invalid contribution count')
    if any(b[0] - a[0] != timedelta(days=1) for a, b in zip(days, days[1:])):
        raise ValueError('Non-contiguous contribution calendar')
    if sum(n for _, n in days) != total:
        raise ValueError('Contribution total mismatch')
    run = longest = active = 0
    for _, n in days:
        active += int(n > 0)
        run = run + 1 if n else 0
        longest = max(longest, run)
    cursor = len(days) - 1
    if days[cursor][0] == today and days[cursor][1] == 0:
        cursor -= 1
    current = 0
    while cursor >= 0 and days[cursor][1] > 0:
        current += 1
        cursor -= 1
    return current, longest, active


def text(x, y, value, size=14, color='#c9d1d9'):
    return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="{color}">{html.escape(str(value))}</text>'


def svg(title, subtitle, body, height=200):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="760" height="{height}" viewBox="0 0 760 {height}">'
            f'<rect x="1" y="1" width="758" height="{height-2}" rx="16" fill="#141321" stroke="#30363d"/>'
            + text(24, 34, title, 22, '#f8fafc') + text(24, 58, subtitle, 12, '#8b949e') + body + '</svg>\n')


def cards(items):
    width = 712 / len(items)
    return ''.join(f'<rect x="{24+i*width:.1f}" y="80" width="{width-8:.1f}" height="82" rx="10" fill="#1f2937"/>'
                   + text(36+i*width, 106, label, 13) + text(36+i*width, 141, value, 24, '#a78bfa')
                   for i, (label, value) in enumerate(items))


def render(profile, repos, languages, days, total, now):
    current, longest, active = metrics(days, total, now.date())
    stamp = now.strftime('%Y-%m-%d %H:%M UTC')
    period = f'{days[0][0]} to {days[-1][0]}'
    stars = sum(r['stargazers_count'] for r in repos)
    forks = sum(r['forks_count'] for r in repos)
    langs = languages.most_common(6)
    lang_total = sum(languages.values())
    bars = ''
    for i, (name, count) in enumerate(langs):
        y = 82 + i*26
        ratio = count / lang_total if lang_total else 0
        bars += text(24, y+13, name, 13) + f'<rect x="190" y="{y}" width="430" height="12" rx="6" fill="#30363d"/><rect x="190" y="{y}" width="{430*ratio:.2f}" height="12" rx="6" fill="#a78bfa"/>' + text(640, y+12, f'{ratio:.1%}', 13)
    if not langs:
        bars = text(24, 100, 'No language data')
    recent = days[-90:]
    peak = max(1, max(n for _, n in recent))
    points = [(24 + i*712/max(1, len(recent)-1), 205 - n*120/peak) for i, (_, n) in enumerate(recent)]
    coords = ' '.join(f'{x:.2f},{y:.2f}' for x, y in points)
    graph = '<line x1="24" y1="205" x2="736" y2="205" stroke="#30363d"/>'
    graph += f'<polyline points="{coords}" fill="none" stroke="#a78bfa" stroke-width="2"/>'
    graph += ''.join(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2" fill="#a78bfa"><title>{d}: {n}</title></circle>' for (x, y), (d, n) in zip(points, recent))
    graph += text(24, 230, recent[0][0], 12) + text(630, 230, recent[-1][0], 12) + text(24, 77, f'Daily peak: {max(n for _, n in recent)}', 12)
    return {
        'github-profile-stats.svg': svg('GitHub Stats', 'Public owned repositories (including forks) | ' + stamp, cards([('Repositories', len(repos)), ('Stars', stars), ('Forks', forks), ('Followers', profile['followers'])])),
        'top-languages.svg': svg('Top Languages', 'Code bytes in public, non-fork repositories | ' + stamp, bars, 252),
        'github-streak.svg': svg('Contribution Streak', period + ' | GitHub-visible contributions', cards([('Current days', current), ('Longest in period', longest), ('Active days', active), ('Contributions', total)])),
        'github-trophy.svg': svg('Repository Summary', 'Public repository metrics | ' + stamp, cards([('Languages', len(languages)), ('Original repos', sum(not r['fork'] for r in repos)), ('Stars', stars), ('Forks', forks)])),
        'contribution-activity.svg': svg('Contribution Activity', f'Last {len(recent)} calendar days | GitHub-visible contributions', graph, 250),
    }


def validate(images):
    for name, content in images.items():
        if ET.fromstring(content).tag != '{http://www.w3.org/2000/svg}svg':
            raise ValueError(f'Invalid SVG: {name}')


def self_test():
    now = datetime(2026, 11, 28, tzinfo=timezone.utc)
    days = [(now.date()-timedelta(days=3-i), n) for i, n in enumerate([1, 2, 3, 0])]
    assert metrics(days, 6, now.date()) == (3, 3, 3)
    try:
        metrics(days, 7, now.date())
    except ValueError:
        pass
    else:
        raise AssertionError('Incorrect totals accepted')
    images = render({'followers': 4}, [{'fork': False, 'stargazers_count': 2, 'forks_count': 1}], Counter({'TypeScript': 75, 'C++ & XML': 25}), days, 6, now)
    validate(images)
    assert '75.0%' in images['top-languages.svg'] and 'Followers' in images['github-profile-stats.svg']
    assert '2026-11-27: 3' in images['contribution-activity.svg']
    print(f'Self-test passed: {len(images)} SVGs, streak, language shares, rejected invalid totals')


if __name__ == '__main__':
    if '--self-test' in sys.argv:
        self_test()
    else:
        images = render(*collect(), datetime.now(timezone.utc))
        validate(images)
        Path('assets').mkdir(exist_ok=True)
        for name, content in images.items():
            Path('assets', name).write_text(content, encoding='utf-8')
        print(f'Generated {len(images)} validated SVGs')
