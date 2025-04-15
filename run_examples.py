import os
import sys
import traceback
from pathlib import Path

examples_dir = "examples"
print("开始运行示例...\n")

# 获取所有示例文件
example_files = [f for f in os.listdir(examples_dir) if f.endswith('.py')]
example_files.sort()

for example_file in example_files:
    print(f"\n正在运行: {example_file}")
    print("-" * 50)
    
    try:
        # 运行示例文件
        example_path = os.path.join(examples_dir, example_file)
        with open(example_path, 'r', encoding='utf-8') as f:
            exec(f.read())
        print(f"成功运行: {example_file}")
    except Exception as e:
        print(f"运行失败: {str(e)}")
        print("\n错误详情:")
        traceback.print_exc()
    
    print("-" * 50)

print("\n所有示例运行完成!") 