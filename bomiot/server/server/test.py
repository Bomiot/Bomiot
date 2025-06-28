import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

API_LIST = [
        # {"name": "测试django", "url": "http://127.0.0.1:8000/test/", "method": "GET"},
        {"name": "测试fastapi", "url": "http://127.0.0.1:8000/fastapi/test/", "method": "GET"},
        # {"name": "测试flask", "url": "http://127.0.0.1:8000/flask/test/", "method": "GET"},
]

CONCURRENCY = 1000
TOTAL_REQUESTS = 10000

def worker(api, idx):
    try:
        start = time.time()
        if api.get("method", "GET").upper() == "POST":
            resp = requests.post(api["url"], data=api.get("data", {}), timeout=10)
        else:
            resp = requests.get(api["url"], params=api.get("params", {}), timeout=10)
        elapsed = time.time() - start
        return (api["name"], resp.status_code, elapsed)
    except Exception as e:
        return (api["name"], str(e), 0)

def main():
    all_results = defaultdict(list)
    start = time.time()
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = []
        for api in API_LIST:
            for i in range(TOTAL_REQUESTS):
                futures.append(executor.submit(worker, api, i))
        for fut in as_completed(futures):
            name, status, elapsed = fut.result()
            all_results[name].append((status, elapsed))
    duration = time.time() - start

    print(f"\n=== API 并发压力测试结果 ===")
    for api in API_LIST:
        name = api["name"]
        results = all_results[name]
        success = [r for r in results if r[0] == 200]
        fail = [r for r in results if r[0] != 200]
        avg_time = sum(r[1] for r in success) / len(success) if success else 0
        print(f"\nAPI: {name}")
        print(f"  总请求: {len(results)}")
        print(f"  成功: {len(success)}")
        print(f"  失败: {len(fail)}")
        print(f"  平均响应时间: {avg_time:.3f}s")
        print(f"  QPS: {len(results)/duration:.2f}")
    print(f"\n总耗时: {duration:.2f}s")

if __name__ == "__main__":
    main()