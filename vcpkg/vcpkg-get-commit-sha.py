import requests
import pandas as pd
from difflib import get_close_matches
import json
import time
import getpass

def get_github_token():
    """获取用户的GitHub token"""
    print("🔑 GitHub Token 设置")
    print("=" * 30)
    print("💡 提示：")
    print("1. 访问 https://github.com/settings/tokens 创建个人访问令牌")
    print("2. 选择 'public_repo' 权限即可")
    print("3. 如果不输入token，将使用匿名访问（限制更严格）")
    print()
    
    use_token = input("是否使用GitHub Token？(y/n): ").strip().lower()
    
    if use_token in ['y', 'yes', '是']:
        # 使用getpass隐藏输入
        token = getpass.getpass("请输入你的GitHub Token: ").strip()
        if token:
            print("✅ Token已设置")
            return token
        else:
            print("⚠️  未输入Token，将使用匿名访问")
            return None
    else:
        print("ℹ️  使用匿名访问")
        return None

def make_github_request(url, headers=None, params=None, max_retries=3, token=None):
    """统一的GitHub API请求函数，包含重试和速率限制处理，增加超时"""
    if headers is None:
        headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 403:
                if token:
                    print("⚠️  GitHub API速率限制，请检查token权限或稍后再试")
                else:
                    print("⚠️  GitHub API速率限制，建议使用GitHub Token")
                return None
            elif response.status_code == 401:
                print("❌ Token无效，请检查你的GitHub Token")
                return None
            elif response.status_code == 404:
                print("❌ 请求的资源不存在")
                return None
            elif response.status_code == 429:
                print(f"⚠️  请求过于频繁，等待 {2 ** attempt} 秒后重试...")
                time.sleep(2 ** attempt)
                continue
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                print(f"❌ 网络请求失败：{e}")
                return None
            else:
                print(f"⚠️  请求失败，{2 ** attempt} 秒后重试...")
                time.sleep(2 ** attempt)
    return None

def get_all_ports(token=None):
    print("🔍 正在获取所有可用的依赖库列表...")
    url = "https://api.github.com/repos/microsoft/vcpkg/git/trees/master?recursive=1"
    response = make_github_request(url, token=token)
    if response is None:
        print("⚠️  使用常见依赖库列表...")
        return get_common_ports()
    data = response.json()
    ports = []
    for item in data.get("tree", []):
        if item["path"].startswith("ports/") and item["type"] == "tree":
            port_name = item["path"].split("/", 1)[1]
            ports.append(port_name)
    print(f"✅ 成功获取 {len(ports)} 个依赖库")
    return ports

def get_common_ports():
    """返回常见的vcpkg依赖库列表"""
    common_ports = [
        # Qt相关
        "qtbase", "qtconnectivity", "qttools", "qtdeclarative", "qtgraphicaleffects",
        "qtimageformats", "qtlocation", "qtmultimedia", "qtnetworkauth", "qtquickcontrols2",
        "qtquickcontrols", "qtscript", "qtscxml", "qtsensors", "qtserialbus", "qtserialport",
        "qtspeech", "qtsvg", "qttranslations", "qtvirtualkeyboard", "qtwebchannel",
        "qtwebengine", "qtwebsockets", "qtwebview", "qtwinextras", "qtx11extras",
        
        # 系统库
        "openssl", "boost", "eigen", "zlib", "bzip2", "libpng", "jpeg", "tiff",
        "freetype", "harfbuzz", "icu", "sqlite3", "mysql", "postgresql", "sqlite",
        
        # 图形库
        "opencv", "sdl2", "glfw", "glew", "glm", "assimp", "bullet", "ogre",
        "vulkan", "vulkan-headers", "vulkan-loader", "vulkan-tools",
        
        # 音频库
        "portaudio", "libsndfile", "flac", "ogg", "vorbis", "opus",
        
        # 网络库
        "curl", "libuv", "asio", "websocketpp", "grpc", "protobuf",
        
        # 压缩库
        "lz4", "zstd", "xz", "7zip", "unrar",
        
        # 其他常用库
        "fmt", "spdlog", "nlohmann-json", "rapidjson", "yaml-cpp", "toml11",
        "gtest", "catch2", "benchmark", "doctest", "cppunit",
        "cmake", "ninja", "pkgconf", "vcpkg-cmake", "vcpkg-cmake-config",
        
        # 开发工具
        "clang", "llvm", "gcc", "mingw", "msys2", "cygwin",
        
        # 数据库
        "redis-plus-plus", "mongocxx", "rocksdb", "leveldb", "lmdb",
        
        # 机器学习
        "tensorflow", "pytorch", "onnx", "opencv-contrib", "dlib",
        
        # 游戏开发
        "box2d", "chipmunk2d", "physfs", "enet", "raknet",
        
        # 多媒体
        "ffmpeg", "gstreamer", "vlc", "mpv", "libav",
        
        # 加密和安全
        "cryptopp", "libsodium", "mbedtls", "wolfssl", "botan",
        
        # 科学计算
        "blas", "lapack", "fftw", "gsl", "armadillo", "itpp",
        
        # 其他
        "pcre", "pcre2", "regex", "boost-regex", "icu", "gettext"
    ]
    
    print(f"✅ 使用常见依赖库列表 ({len(common_ports)} 个)")
    return common_ports

def find_similar_ports(target_port, all_ports, n=5):
    """查找与目标port名称最相似的n个唯一port，保留原始大小写"""
    if not all_ports:
        return []
    # 用dict去重并保留原始大小写
    lower_to_original = {port.lower(): port for port in all_ports}
    similar_lowers = get_close_matches(target_port.lower(), list(lower_to_original.keys()), n=n, cutoff=0.3)
    # 保证推荐唯一且顺序合理
    result = []
    for lower in similar_lowers:
        if lower in lower_to_original:
            result.append(lower_to_original[lower])
    return result

def get_port_versions(port_name, token=None):
    """获取指定port的所有可用版本"""
    print(f"📦 正在查询 {port_name} 的所有版本...")
    
    try:
        # 获取port目录下的内容
        url = f"https://api.github.com/repos/microsoft/vcpkg/contents/ports/{port_name}"
        
        response = make_github_request(url, token=token)
        if response is None:
            return ["最新版本"]
        
        data = response.json()
        
        versions = []
        for item in data:
            if item["type"] == "file" and item["name"].endswith(".json"):
                # 尝试解析vcpkg.json文件来获取版本信息
                try:
                    file_url = item["download_url"]
                    file_response = make_github_request(file_url, token=token)
                    if file_response is None:
                        continue
                        
                    file_data = json.loads(file_response.text)
                    
                    if "version" in file_data:
                        versions.append(file_data["version"])
                    elif "versions" in file_data:
                        for version_info in file_data["versions"]:
                            if "version" in version_info:
                                versions.append(version_info["version"])
                except:
                    continue
        
        return versions if versions else ["最新版本"]
        
    except Exception as e:
        print(f"❌ 获取版本信息失败：{e}")
        return ["最新版本"]

def get_latest_commit_sha(port_name, token=None):
    """获取指定port的最新commit SHA"""
    repo = "microsoft/vcpkg"
    path = f"ports/{port_name}"

    url = f"https://api.github.com/repos/{repo}/commits"
    params = {"path": path, "per_page": 1}

    print(f"📦 正在查询 {port_name} 的最新 commit SHA...")

    try:
        response = make_github_request(url, params=params, token=token)
        if response is None:
            return "无法获取"

        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            return data[0]["sha"]
        else:
            return "找不到"

    except Exception as e:
        print(f"❌ 错误：{e}")
        return "异常"

def get_port_versions_and_shas(port_name):
    """
    更快地查找指定port的所有版本及其commit SHA，兼容没有version字段的情况
    """
    import requests, json
    # 1. 获取所有json文件路径
    url = "https://api.github.com/repos/microsoft/vcpkg/git/trees/master?recursive=1"
    resp = requests.get(url, timeout=15)
    if resp.status_code != 200:
        return []
    data = resp.json()
    # 2. 找到目标端口的json文件
    target_path = None
    for item in data.get("tree", []):
        if item["path"].startswith("versions/") and item["path"].endswith(f"/{port_name}.json"):
            target_path = item["path"]
            break
    if not target_path:
        return []
    # 3. 下载该json文件
    raw_url = f"https://raw.githubusercontent.com/microsoft/vcpkg/master/{target_path}"
    resp2 = requests.get(raw_url, timeout=10)
    if resp2.status_code != 200:
        return []
    data2 = json.loads(resp2.text)
    if "versions" in data2:
        result = []
        for v in data2["versions"]:
            version = v.get("version") or v.get("version-date") or v.get("port-version") or "N/A"
            sha = v.get("git-tree", "")
            result.append((version, sha))
        return result
    return []

def main():
    print("🚀 vcpkg 依赖库查询工具")
    print("=" * 50)
    
    # 获取GitHub token
    token = get_github_token()
    
    if token:
        print(f"✅ 使用GitHub Token，API限制：5000次/小时")
    else:
        print("ℹ️  使用匿名访问，API限制：60次/小时")
    
    print()
    
    # 获取所有可用的ports
    all_ports = get_all_ports(token)
    
    while True:
        # 询问用户想要查询的依赖库
        port_name = input("\n🔍 请输入你想要查询的依赖库名称 (输入 'quit' 退出): ").strip()
        
        if port_name.lower() == 'quit':
            print("👋 再见！")
            break
        
        if not port_name:
            print("❌ 请输入有效的依赖库名称")
            continue
        
        # 检查port是否存在
        if port_name not in all_ports:
            print(f"❌ 未找到依赖库 '{port_name}'")
            
            # 查找相似的port名称
            similar_ports = find_similar_ports(port_name, all_ports)
            if similar_ports:
                print(f"  也许你想要的是以下这些依赖库：")
                for i, similar in enumerate(similar_ports, 1):
                    print(f"   {i}. {similar}")
                print("\n请重新输入正确的依赖库名称")
            continue
        
        # 新增：获取所有版本及其commit SHA
        print(f"📋 {port_name} 的所有版本及其 commit SHA：")
        versions_and_shas = get_port_versions_and_shas(port_name)
        if versions_and_shas:
            # 输出表头
            print(f"{'版本':<20} {'commit SHA':<40}")
            print('-' * 60)
            for version, sha in versions_and_shas:
                print(f"{version:<20} {sha:<40}")
        else:
            print("未能获取到该依赖库的版本及commit SHA信息。")
        
        # 兼容原有逻辑，继续支持单版本选择和commit SHA
        versions = get_port_versions(port_name, token)
        if len(versions) > 1:
            print(f"\n📋 {port_name} 的所有可用版本：")
            for i, version in enumerate(versions, 1):
                print(f"   {i}. {version}")
            try:
                choice = input(f"\n请选择版本 (1-{len(versions)}) 或直接回车使用最新版本: ").strip()
                if choice and choice.isdigit():
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(versions):
                        selected_version = versions[choice_idx]
                    else:
                        selected_version = versions[0]
                else:
                    selected_version = versions[0]
            except:
                selected_version = versions[0]
        else:
            selected_version = versions[0]
        print(f"\n✅ 选择的版本: {selected_version}")
        commit_sha = get_latest_commit_sha(port_name, token)
        print(f"\n📋 查询结果：")
        print(f"依赖库: {port_name}")
        print(f"版本: {selected_version}")
        print(f"最新Commit SHA: {commit_sha}")
        continue_query = input("\n是否继续查询其他依赖库？(y/n): ").strip().lower()
        if continue_query not in ['y', 'yes', '是']:
            print("👋 再见！")
            break

if __name__ == "__main__":
    main()
