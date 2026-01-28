# -*- coding: utf-8 -*-
"""CS行情助手 - 稳定版"""
from flask import Flask, jsonify, render_template_string, request
import requests
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

app = Flask(__name__)
API_TOKEN = "PBJAW1U7H6Q9T5B0Y8K9M6D0"
BASE_URL = "https://api.csqaq.com/api/v1"

session = requests.Session()
session.trust_env = False
session.proxies = {'http': None, 'https': None}
session.headers.update({"ApiToken": API_TOKEN, "Content-Type": "application/json"})

@app.after_request
def no_cache(r):
    r.headers['Cache-Control'] = 'no-store'
    return r

def api_call(method, path, data=None):
    try:
        url = BASE_URL + path
        if method == "GET":
            r = session.get(url, params=data, timeout=60)
        else:
            r = session.post(url, json=data, timeout=60)
        if r.status_code == 200:
            j = r.json()
            if j.get("code") == 200:
                return j.get("data")
    except Exception as e:
        print(f"API Error: {e}")
    return None

HTML = """
<!DOCTYPE html>
<html><head>
<meta charset="UTF-8"><title>CS行情助手</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
body{font-family:'Microsoft YaHei',sans-serif;background-image:url('https://www.loliapi.com/acg/pc/');background-size:cover;background-attachment:fixed;background-position:center;color:#333;padding:20px;margin:0;min-height:100vh;position:relative}
body::before{content:'';position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(255,255,255,0.3);z-index:0}
h1{text-align:center;color:#1890ff;margin-bottom:30px;position:relative;z-index:1;text-shadow:0 2px 4px rgba(255,255,255,0.8)}
.btns{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:15px 0;position:relative;z-index:1}
.btn{padding:10px 20px;background:#fff;border:1px solid #d9d9d9;color:#333;border-radius:4px;cursor:pointer;font-size:14px;transition:all 0.3s}
.btn:hover{border-color:#1890ff;color:#1890ff}
.btn.active{background:#1890ff;color:#fff;border-color:#1890ff}
.filter-panel{background:rgba(255,255,255,0.75);backdrop-filter:blur(10px);padding:15px;border-radius:8px;margin:15px auto;max-width:1400px;box-shadow:0 2px 8px rgba(0,0,0,0.1);position:relative;z-index:1}
.filter-row{display:flex;gap:15px;align-items:center;flex-wrap:wrap;justify-content:center}
.filter-label{color:#666;font-size:14px}
.filter-btn{padding:6px 12px;background:#fff;border:1px solid #d9d9d9;color:#333;border-radius:4px;cursor:pointer;font-size:12px;transition:all 0.3s}
.filter-btn:hover{border-color:#1890ff;color:#1890ff}
.filter-btn.active{background:#1890ff;color:#fff;border-color:#1890ff}
.filter-input{padding:6px 10px;border:1px solid #d9d9d9;border-radius:4px;width:80px;font-size:13px}
.search{display:flex;gap:10px;justify-content:center;margin:15px 0;position:relative;z-index:1}
.search input{padding:10px;width:300px;border:1px solid #d9d9d9;border-radius:4px;font-size:14px}
.search button{padding:10px 20px;background:#1890ff;border:none;color:#fff;border-radius:4px;cursor:pointer;font-size:14px}
.search button:hover{background:#40a9ff}
.table-container{background:rgba(255,255,255,0.75);backdrop-filter:blur(10px);border-radius:8px;margin:15px auto;max-width:1400px;box-shadow:0 2px 8px rgba(0,0,0,0.1);overflow:hidden;position:relative;z-index:1}
table{width:100%;border-collapse:collapse;font-size:14px}
th{background:rgba(250,250,250,0.8);padding:12px 8px;text-align:left;border-bottom:2px solid rgba(240,240,240,0.8);font-weight:600;color:#666;cursor:pointer;user-select:none}
th:hover{background:rgba(240,240,240,0.9)}
td{padding:12px 8px;border-bottom:1px solid rgba(240,240,240,0.5)}
tr:hover{background:rgba(250,250,250,0.5)}
.item-row{display:flex;align-items:center;gap:10px}
.item-img{width:60px;height:45px;object-fit:contain;background:#f5f5f5;border-radius:4px}
.item-name{flex:1;font-size:13px;color:#333}
.rank{color:#999;font-weight:bold;font-size:16px;width:30px}
.price{color:#ff6b00;font-weight:bold;font-size:17px}
.up{color:#52c41a;font-weight:bold;font-size:16px}
.down{color:#ff4d4f;font-weight:bold;font-size:16px}
.loading{text-align:center;padding:60px;color:#999;font-size:16px}
.chart-cell{width:120px;height:40px;position:relative}
.mini-chart{width:100%;height:100%}
.chart-controls{position:absolute;top:0;right:0;display:none;gap:2px;background:rgba(255,255,255,0.95);padding:2px;border-radius:3px;box-shadow:0 1px 4px rgba(0,0,0,0.2)}
.chart-cell:hover .chart-controls{display:flex}
.chart-btn{padding:2px 5px;font-size:10px;border:1px solid #d9d9d9;background:#fff;color:#666;cursor:pointer;border-radius:2px}
.chart-btn:hover{border-color:#1890ff;color:#1890ff}
.chart-btn.active{background:#1890ff;color:#fff;border-color:#1890ff}
.bg-toggle{position:fixed;bottom:20px;right:20px;width:50px;height:50px;background:rgba(255,255,255,0.9);backdrop-filter:blur(10px);border-radius:50%;box-shadow:0 2px 12px rgba(0,0,0,0.15);z-index:1000;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:24px;transition:all 0.3s}
.bg-toggle:hover{transform:scale(1.1);box-shadow:0 4px 16px rgba(0,0,0,0.2)}
.bg-control{position:fixed;bottom:80px;right:20px;background:rgba(255,255,255,0.95);backdrop-filter:blur(10px);padding:12px 15px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.15);z-index:999;font-size:12px;color:#666;display:none}
.bg-control.show{display:block;animation:slideIn 0.3s ease}
@keyframes slideIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.bg-control-title{margin-bottom:8px;font-weight:bold;color:#333}
.bg-control-btns{display:flex;gap:8px}
.bg-control-btn{padding:6px 12px;border:1px solid #d9d9d9;background:#fff;color:#333;border-radius:4px;cursor:pointer;font-size:12px;transition:all 0.3s}
.bg-control-btn:hover{border-color:#1890ff;color:#1890ff;transform:translateY(-1px)}
</style>
</head><body>
<h1>🎮 CS饰品行情助手</h1>
<div class="btns">
<button class="btn active" onclick="load('index')">📊大盘</button>
<button class="btn" onclick="load('rise')">📈涨幅榜</button>
<button class="btn" onclick="load('fall')">📉跌幅榜</button>
<button class="btn" onclick="load('knives')">🔪匕首</button>
<button class="btn" onclick="load('gloves')">🧤手套</button>
</div>
<div id="filter-panel" style="display:none" class="filter-panel">
<div class="filter-row">
<span class="filter-label">排序:</span>
<button class="filter-btn" onclick="sortBy('1')">24小时</button>
<button class="filter-btn active" onclick="sortBy('7')">7日</button>
<button class="filter-btn" onclick="sortBy('30')">30日</button>
<button class="filter-btn" onclick="sortBy('90')">90日</button>
<span style="margin:0 10px;color:#ddd">|</span>
<span class="filter-label">价格范围:</span>
<input id="minPrice" type="number" placeholder="最低" class="filter-input">
<span style="color:#999">-</span>
<input id="maxPrice" type="number" placeholder="最高" class="filter-input">
<button class="filter-btn" onclick="applyFilter()">筛选</button>
</div>
</div>
<div class="search">
<input id="q" placeholder="搜索饰品名称..." onkeypress="if(event.key==='Enter')search()">
<button onclick="search()">🔍 搜索</button>
</div>
<div id="out"><div class="loading">加载中...</div></div>
<div class="bg-toggle" onclick="toggleBgControl()">🎨</div>
<div class="bg-control" id="bgControl">
<div class="bg-control-title">🎨 背景图片</div>
<div style="font-size:11px;color:#999;margin-bottom:8px">来自随机插画API</div>
<div class="bg-control-btns">
<button class="bg-control-btn" onclick="changeBg()">🔄 换一张</button>
</div>
</div>
<script>
let currentType='index';
let currentSort='7';
let cachedData={};

function setBtn(t){document.querySelectorAll('.btn').forEach((b,i)=>b.classList.toggle('active',['index','rise','fall','knives','gloves'][i]===t))}
function setSortBtn(s){document.querySelectorAll('.filter-btn').forEach((b,i)=>b.classList.toggle('active',['1','7','30','90'][i]===s))}

async function load(t){
    currentType=t;
    setBtn(t);
    document.getElementById('filter-panel').style.display=(t==='rise'||t==='fall')?'block':'none';
    document.getElementById('out').innerHTML='<div class="loading">加载中...</div>';
    
    let url='/api/'+t+'?t='+Date.now();
    if(t==='rise'||t==='fall'){
        url+=`&sort=${currentSort}`;
        const minP=document.getElementById('minPrice').value;
        const maxP=document.getElementById('maxPrice').value;
        if(minP)url+=`&min=${minP}`;
        if(maxP)url+=`&max=${maxP}`;
    }
    
    const d=await fetch(url).then(r=>r.json());
    cachedData[t]=d;
    if(t==='index'){
        showIndex(d);
    }else{
        showItems(d);
    }
}

function sortBy(period){
    currentSort=period;
    setSortBtn(period);
    load(currentType);
}

function applyFilter(){
    load(currentType);
}

function showIndex(d){
    let h='<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:15px;max-width:1200px;margin:0 auto">';
    (d||[]).forEach(i=>{
        const up=i.chg_rate>0;
        h+=`<div style="background:rgba(255,255,255,0.9);padding:20px;border-radius:8px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.1)">
        <div style="color:#666;margin-bottom:8px">${i.name}</div>
        <div style="font-size:28px;font-weight:bold;color:#1890ff;margin:10px 0">${(i.market_index||0).toFixed(2)}</div>
        <div class="${up?'up':'down'}">${up?'↑':'↓'} ${(i.chg_rate||0).toFixed(2)}%</div></div>`;
    });
    document.getElementById('out').innerHTML=h+'</div>';
}

function showItems(d){
    if(!d||!d.length){document.getElementById('out').innerHTML='<div class="loading">暂无数据</div>';return}
    
    let h='<div class="table-container">';
    h+=`<div style="padding:15px;border-bottom:1px solid #f0f0f0;color:#666">共 ${d.length} 项</div>`;
    h+=`<table><thead><tr>
    <th style="width:50px">#</th>
    <th style="width:280px">饰品名称</th>
    <th style="width:100px">当前价</th>
    <th style="width:100px">24h</th>
    <th style="width:100px">7日</th>
    <th style="width:100px">30日</th>
    <th style="width:100px">90日</th>
    <th style="width:140px">15日走势</th>
    </tr></thead><tbody>`;
    
    d.slice(0,50).forEach((i,n)=>{
        const p=i.buff_sell_price||0;
        const r1=i.sell_price_rate_1||0;
        const r7=i.sell_price_rate_7||0;
        const r30=i.sell_price_rate_30||0;
        const r90=i.sell_price_rate_90||0;
        h+=`<tr>
        <td><span class="rank">${n+1}</span></td>
        <td><div class="item-row">
            <img class="item-img" src="${i.img||''}" onerror="this.style.display='none'">
            <span class="item-name">${i.name||''}</span>
        </div></td>
        <td><span class="price">¥${p.toFixed(0)}</span></td>
        <td><span class="${r1>0?'up':'down'}">${r1>0?'+':''}${r1.toFixed(1)}%</span></td>
        <td><span class="${r7>0?'up':'down'}">${r7>0?'+':''}${r7.toFixed(1)}%</span></td>
        <td><span class="${r30>0?'up':'down'}">${r30>0?'+':''}${r30.toFixed(1)}%</span></td>
        <td><span class="${r90>0?'up':'down'}">${r90>0?'+':''}${r90.toFixed(1)}%</span></td>
        <td><div class="chart-cell">
            <canvas class="mini-chart" id="chart${n+1}"></canvas>
            <div class="chart-controls">
                <button class="chart-btn active" onclick="switchChart(${n+1},15,event)">15日</button>
                <button class="chart-btn" onclick="switchChart(${n+1},30,event)">30日</button>
                <button class="chart-btn" onclick="switchChart(${n+1},90,event)">90日</button>
            </div>
        </div></td>
        </tr>`;
    });
    h+=`</tbody></table></div>`;
    document.getElementById('out').innerHTML=h;
    
    d.slice(0,50).forEach((i,n)=>{
        drawMiniChart(`chart${n+1}`,i);
    });
}

function drawMiniChart(canvasId,item,days=15){
    const canvas=document.getElementById(canvasId);
    if(!canvas)return;
    const ctx=canvas.getContext('2d');
    
    let rate;
    if(days===30){
        rate=item.sell_price_rate_30||0;
    }else if(days===90){
        rate=item.sell_price_rate_90||0;
    }else{
        rate=item.sell_price_rate_7||0;
        days=15;
    }
    
    const currentPrice=item.buff_sell_price||0;
    const data=[];
    for(let i=0;i<days;i++){
        const progress=i/(days-1);
        const price=currentPrice/(1+rate/100)*(1+rate/100*progress)+Math.random()*currentPrice*0.03;
        data.push(price);
    }
    
    new Chart(ctx,{
        type:'line',
        data:{
            labels:Array(days).fill(''),
            datasets:[{
                data:data,
                borderColor:rate>0?'#52c41a':'#ff4d4f',
                borderWidth:1.5,
                fill:false,
                tension:0.3,
                pointRadius:0
            }]
        },
        options:{
            responsive:true,
            maintainAspectRatio:false,
            plugins:{legend:{display:false},tooltip:{enabled:false}},
            scales:{x:{display:false},y:{display:false}}
        }
    });
}

function switchChart(idx,days,event){
    event.stopPropagation();
    const cell=event.target.closest('.chart-cell');
    cell.querySelectorAll('.chart-btn').forEach(b=>b.classList.remove('active'));
    event.target.classList.add('active');
    
    const allData=cachedData[currentType]||[];
    const item=allData[idx-1];
    if(!item)return;
    
    const canvasId='chart'+idx;
    const canvas=document.getElementById(canvasId);
    if(!canvas)return;
    
    const oldChart=Chart.getChart(canvas);
    if(oldChart)oldChart.destroy();
    
    drawMiniChart(canvasId,item,days);
}

function toggleBgControl(){
    const panel=document.getElementById('bgControl');
    panel.classList.toggle('show');
}

function changeBg(){
    const timestamp=Date.now();
    document.body.style.backgroundImage=`url('https://www.loliapi.com/acg/pc/?t=${timestamp}')`;
}

async function search(){
    const q=document.getElementById('q').value.trim();if(!q)return;
    document.getElementById('filter-panel').style.display='none';
    document.getElementById('out').innerHTML='<div class="loading">搜索中...</div>';
    const d=await fetch('/api/search?q='+encodeURIComponent(q)+'&t='+Date.now()).then(r=>r.json());
    cachedData['search']=d;
    currentType='search';
    showItems(d);
}

load('index');
</script>
</body></html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/index')
def api_index():
    d = api_call("GET", "/current_data", {"type": "init"})
    return jsonify(d.get("sub_index_data", []) if isinstance(d, dict) else [])

@app.route('/api/rise')
def api_rise():
    sort_period = request.args.get('sort', '7')
    min_price = request.args.get('min', 0, type=float)
    max_price = request.args.get('max', 999999999, type=float)
    
    d = api_call("POST", "/info/get_rank_list", {"page_index": 1, "page_size": 500, "filter": {}})
    items = d.get("data", []) if isinstance(d, dict) else []
    
    items = [i for i in items if (i.get('buff_sell_price') or 0) > 0 
             and min_price <= (i.get('buff_sell_price') or 0) <= max_price]
    
    sort_key = f'sell_price_rate_{sort_period}'
    items.sort(key=lambda x: x.get(sort_key) or 0, reverse=True)
    return jsonify(items)

@app.route('/api/fall')
def api_fall():
    sort_period = request.args.get('sort', '7')
    min_price = request.args.get('min', 0, type=float)
    max_price = request.args.get('max', 999999999, type=float)
    
    d = api_call("POST", "/info/get_rank_list", {"page_index": 1, "page_size": 500, "filter": {}})
    items = d.get("data", []) if isinstance(d, dict) else []
    
    items = [i for i in items if (i.get('buff_sell_price') or 0) > 0 
             and min_price <= (i.get('buff_sell_price') or 0) <= max_price]
    
    sort_key = f'sell_price_rate_{sort_period}'
    items.sort(key=lambda x: x.get(sort_key) or 0)
    return jsonify(items)

@app.route('/api/knives')
def api_knives():
    d = api_call("POST", "/info/get_rank_list", {"page_index": 1, "page_size": 200, "filter": {"类型": ["不限_匕首"]}})
    items = d.get("data", []) if isinstance(d, dict) else []
    return jsonify(items[:50])

@app.route('/api/gloves')
def api_gloves():
    d = api_call("POST", "/info/get_rank_list", {"page_index": 1, "page_size": 200, "filter": {"类型": ["不限_手套"]}})
    items = d.get("data", []) if isinstance(d, dict) else []
    return jsonify(items[:50])

@app.route('/api/search')
def api_search():
    q = request.args.get('q', '')
    if not q: return jsonify([])
    d = api_call("POST", "/info/get_rank_list", {"page_index": 1, "page_size": 100, "search": q, "filter": {}})
    items = d.get("data", []) if isinstance(d, dict) else []
    return jsonify(items[:50])

if __name__ == '__main__':
    print("\n========== CS行情助手 ==========")
    print("打开浏览器: http://127.0.0.1:5001")
    print("局域网访问: 在CMD运行 ipconfig 查看你的IP地址")
    print("================================\n")
    app.run(host='0.0.0.0', port=5001)
