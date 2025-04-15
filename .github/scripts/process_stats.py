import os
import json
import re
import requests
from datetime import datetime

# 获取环境变量
issue_title = os.environ.get('ISSUE_TITLE', '')
issue_body = os.environ.get('ISSUE_BODY', '')
github_token = os.environ.get('GITHUB_TOKEN', '')

# 从Issue标题中提取版本和设备ID
match = re.search(r'Usage Stats: v([\d\.]+) \| ([a-f0-9]+)', issue_title)
if match:
    version = match.group(1)
    device_id = match.group(2)
    
    # 从Issue正文中提取时间戳
    timestamp_match = re.search(r'\*\*时间戳\*\*: `([^`]+)`', issue_body)
    timestamp = timestamp_match.group(1) if timestamp_match else datetime.now().isoformat()
    
    # 读取现有统计数据
    stats_file = 'stats/usage_stats.json'
    stats = {}
    
    try:
        # 获取现有文件（如果存在）
        response = requests.get(
            f'https://api.github.com/repos/{os.environ["GITHUB_REPOSITORY"]}/contents/{stats_file}',
            headers={'Authorization': f'token {github_token}'}
        )
        
        if response.status_code == 200:
            content = response.json()
            stats = json.loads(requests.get(content['download_url']).text)
    except:
        stats = {'versions': {}, 'devices': {}}
    
    # 更新统计数据
    if 'versions' not in stats:
        stats['versions'] = {}
    if 'devices' not in stats:
        stats['devices'] = {}
    
    # 更新版本统计
    if version not in stats['versions']:
        stats['versions'][version] = {'count': 0, 'last_seen': ''}
    stats['versions'][version]['count'] += 1
    stats['versions'][version]['last_seen'] = timestamp
    
    # 更新设备统计
    if device_id not in stats['devices']:
        stats['devices'][device_id] = {'first_seen': timestamp, 'versions': []}
    if version not in stats['devices'][device_id]['versions']:
        stats['devices'][device_id]['versions'].append(version)
    
    # 确保目录存在
    os.makedirs('stats', exist_ok=True)
    
    # 保存更新后的统计数据
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    
    # 提交更新后的文件
    with open(stats_file, 'rb') as f:
        content = f.read()
    
    # 获取当前文件的SHA（如果存在）
    sha = None
    try:
        response = requests.get(
            f'https://api.github.com/repos/{os.environ["GITHUB_REPOSITORY"]}/contents/{stats_file}',
            headers={'Authorization': f'token {github_token}'}
        )
        if response.status_code == 200:
            sha = response.json()['sha']
    except:
        pass
    
    # 提交更新
    response = requests.put(
        f'https://api.github.com/repos/{os.environ["GITHUB_REPOSITORY"]}/contents/{stats_file}',
        headers={'Authorization': f'token {github_token}'},
        json={
            'message': f'Update usage statistics for v{version}',
            'content': content.decode('utf-8'),
            'sha': sha
        }
    )
    
    print(f'Updated statistics for version {version}, device {device_id}')
else:
    print('Invalid issue title format')
