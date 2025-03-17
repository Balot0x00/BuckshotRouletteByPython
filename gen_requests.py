import os
import re
import pkg_resources

def ExtractImports(file_path):
    """ 从 Python 文件中提取 import 语句 """
    imports = set()
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(r"^\s*(?:import|from)\s+([a-zA-Z0-9_]+)", line)
            if match:
                imports.add(match.group(1))
    return imports

def GetInstalledPackages():
    """ 获取已安装的库名称（避免系统库） """
    return {pkg.key for pkg in pkg_resources.working_set}

def ScanFolderForImports(folder):
    """ 扫描文件夹中所有 .py 文件，提取 import 并生成 requirements.txt """
    all_imports = set()
    installed_packages = GetInstalledPackages()

    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                all_imports.update(ExtractImports(file_path))

    # 过滤掉标准库，仅保留第三方库
    third_party_libs = sorted(all_imports.intersection(installed_packages))

    # 写入 requirements.txt
    with open("requirements.txt", "w", encoding="utf-8") as f:
        for lib in third_party_libs:
            f.write(lib + "\n")

    print("✅ 已生成 requirements.txt")

# 执行扫描
ScanFolderForImports(".")  # 当前目录
