import requests
import pandas as pd

def get_latest_commit_sha(port_name):
    # GitHub repo and path to the port
    repo = "microsoft/vcpkg"
    path = f"ports/{port_name}"

    url = f"https://api.github.com/repos/{repo}/commits"
    params = {"path": path, "per_page": 1}
    headers = {"Accept": "application/vnd.github+json"}

    print(f"📦 正在查询 {port_name} 的最新 commit SHA...")

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            return data[0]["sha"]
        else:
            return "找不到"

    except Exception as e:
        print(f"❌ 错误：{e}")
        return "异常"

# 要查询的 ports 列表
ports = ["qtbase", "qtconnectivity", "qttools"]
results = [{"port": port, "sha": get_latest_commit_sha(port)} for port in ports]

df = pd.DataFrame(results)
print("\n📋 查询结果：")
print(df)
