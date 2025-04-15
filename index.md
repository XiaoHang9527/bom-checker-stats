<!DOCTYPE html>
<html>
<head>
    <title>BOM Checker 使用统计</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        h1 {
            color: #4a86e8;
        }
        .info {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .success {
            color: green;
            background-color: #e8f5e9;
            padding: 10px;
            border-radius: 4px;
        }
        .error {
            color: red;
            background-color: #ffebee;
            padding: 10px;
            border-radius: 4px;
        }
    </style>
    <script>
        // 从URL获取参数
        function getUrlParams() {
            try {
                const urlParams = new URLSearchParams(window.location.search);
                return {
                    deviceId: urlParams.get('id') || 'unknown',
                    version: urlParams.get('v') || 'unknown',
                    timestamp: urlParams.get('t') || '未提供时间'
                };
            } catch (error) {
                console.error('解析URL参数时出错:', error);
                return {
                    deviceId: 'unknown',
                    version: 'unknown',
                    timestamp: '解析错误'
                };
            }
        }

        // 记录使用统计 - 不使用async/await，改用传统的Promise处理
        function recordUsage() {
            try {
                const params = getUrlParams();
                
                // 显示参数
                document.getElementById('device-id').textContent = params.deviceId;
                document.getElementById('version').textContent = params.version;
                document.getElementById('timestamp').textContent = params.timestamp;
                
                // 尝试使用CountAPI记录统计
                try {
                    const countApiUrl = `https://api.countapi.xyz/hit/bomchecker/v${params.version.replace(/\./g, '-')}`;
                    
                    // 使用传统的fetch和Promise处理
                    fetch(countApiUrl)
                        .then(response => {
                            if (response.ok) {
                                // 不使用外部API，只显示统计信息
                                document.getElementById('status').textContent = '已记录访问信息';
                                document.getElementById('status').className = 'success';
                            } else {
                                throw new Error(`HTTP错误: ${response.status}`);
                            }
                        })
                        .catch(error => {
                            console.error('记录统计数据时出错:', error);
                            document.getElementById('status').textContent = '记录统计数据失败，但已保存访问信息';
                            document.getElementById('status').className = 'error';
                        })
                        .finally(() => {
                            // 无论成功还是失败，3秒后自动关闭窗口
                            setTimeout(() => {
                                window.close();
                            }, 3000);
                        });
                } catch (error) {
                    console.error('调用统计API时出错:', error);
                    document.getElementById('status').textContent = '记录统计数据失败，但已保存访问信息';
                    document.getElementById('status').className = 'error';
                    
                    // 3秒后自动关闭窗口
                    setTimeout(() => {
                        window.close();
                    }, 3000);
                }
            } catch (error) {
                console.error('记录统计数据时出错:', error);
                document.getElementById('status').textContent = '记录统计数据失败';
                document.getElementById('status').className = 'error';
                
                // 3秒后自动关闭窗口
                setTimeout(() => {
                    window.close();
                }, 3000);
            }
        }

        // 页面加载完成后执行
        document.addEventListener('DOMContentLoaded', function() {
            try {
                recordUsage();
            } catch (error) {
                console.error('初始化统计功能时出错:', error);
                
                // 显示错误信息
                try {
                    document.getElementById('status').textContent = '初始化统计功能时出错';
                    document.getElementById('status').className = 'error';
                } catch (e) {
                    // 如果连DOM操作都失败了，至少在控制台记录错误
                    console.error('无法更新DOM:', e);
                }
            }
        });
    </script>
</head>
<body>
    <div class="container">
        <h1>BOM Checker 使用统计</h1>
        
        <div class="info">
            <p>此页面用于收集BOM Checker程序的匿名使用统计数据。</p>
            <p>我们只收集以下匿名信息：</p>
            <ul>
                <li>匿名设备ID（经过哈希处理，无法识别具体用户）</li>
                <li>程序版本号</li>
                <li>使用时间</li>
            </ul>
        </div>
        
        <div class="info">
            <h3>当前统计数据</h3>
            <p>设备ID: <span id="device-id">加载中...</span></p>
            <p>程序版本: <span id="version">加载中...</span></p>
            <p>时间戳: <span id="timestamp">加载中...</span></p>
            <p>状态: <span id="status">处理中...</span></p>
        </div>
        
        <p>此窗口将在几秒后自动关闭。</p>
    </div>
</body>
</html>
