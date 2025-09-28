#!/usr/bin/env python3
"""
安装脚本，用于创建虚拟环境并安装项目依赖
"""

import os
import sys
import subprocess
import venv

def create_virtual_environment():
    """创建虚拟环境"""
    venv_dir = os.path.join(os.path.dirname(__file__), 'venv')
    if not os.path.exists(venv_dir):
        print("创建虚拟环境...")
        venv.create(venv_dir, with_pip=True)
        print(f"虚拟环境已创建: {venv_dir}")
    else:
        print("虚拟环境已存在")
    
    return venv_dir

def install_dependencies(venv_dir):
    """在虚拟环境中安装依赖"""
    # 获取虚拟环境中的pip路径
    if sys.platform == "win32":
        pip_path = os.path.join(venv_dir, 'Scripts', 'pip')
    else:
        pip_path = os.path.join(venv_dir, 'bin', 'pip')
    
    # 升级pip
    print("升级pip...")
    subprocess.run([pip_path, "install", "--upgrade", "pip"])
    
    # 安装项目依赖
    print("安装项目依赖...")
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    subprocess.run([pip_path, "install", "-r", requirements_path])
    
    print("依赖安装完成!")

def main():
    """主函数"""
    print("开始安装AI雷达项目依赖...")
    
    try:
        # 创建虚拟环境
        venv_dir = create_virtual_environment()
        
        # 安装依赖
        install_dependencies(venv_dir)
        
        print("\n安装完成!")
        print("要激活虚拟环境，请运行:")
        if sys.platform == "win32":
            print(f"  {os.path.join(venv_dir, 'Scripts', 'activate')}")
        else:
            print(f"  source {os.path.join(venv_dir, 'bin', 'activate')}")
            
    except Exception as e:
        print(f"安装过程中出现错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()