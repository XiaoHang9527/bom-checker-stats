<!DOCTYPE html>
<html>
<head>
    <title>BOM Checker 使用统计</title>
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
    </style>
    <script>
        // 从URL获取参数
        function getUrlParams() {
            const urlParams = new URLSearchParams(window.location.search);
            return {
                deviceId: urlParams.get('id') || 'unknown',
                version: urlParams.get('v') || 'unknown',
                timestamp: urlParams.get('t') || '未提供时间'
            };
        }

        // 记录使用统计
        async function recordUsage() {
            try {
                const params = getUrlParams();
                
                // 方法2：使用CountAPI（简单的计数器API）
                const countApiUrl = `https://api.countapi.xyz/hit/bomchecker/v${params.version.replace(/\./g, '-')}`;
                await fetch(countApiUrl);
                
                // 显示成功消息
                document.getElementById('status').textContent = '统计数据已记录';
                document.getElementById('status').className = 'success';
                
                // 3秒后自动关闭窗口
                setTimeout(() => {
                    window.close();
                }, 3000);
            } catch (error) {
                console.error('记录统计数据时出错:', error);
                document.getElementById('status').textContent = '记录统计数据失败';
                document.getElementById('status').style.color = 'red';
            }
        }

        // 页面加载完成后执行
        window.addEventListener('DOMContentLoaded', function() {
            const params = getUrlParams();
            
            // 显示参数 - 直接显示原始字符串，不进行任何转换
            document.getElementById('device-id').textContent = params.deviceId;
            document.getElementById('version').textContent = params.version;
            document.getElementById('timestamp').textContent = params.timestamp;
            
            // 记录使用统计
            recordUsage();
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
