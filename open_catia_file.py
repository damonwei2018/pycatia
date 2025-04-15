from pycatia import catia
import os
import time

# 指定目录路径 - 使用相对路径
directory = os.path.join(os.getcwd(), "models", "Yun_100_Sdeven_20140716")

def list_catia_files(directory):
    """列出目录中的CATIA文件"""
    files = os.listdir(directory)
    return sorted([f for f in files if f.endswith(('.CATPart', '.CATProduct'))])

def get_file_info(filepath):
    """获取文件信息"""
    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    return f"{size_mb:.2f} MB"

try:
    # 检查目录是否存在
    if not os.path.exists(directory):
        print(f"错误：目录不存在: {directory}")
        exit()
    else:
        print(f"成功找到目录: {directory}")
    
    # 连接到CATIA
    caa = catia()
    print("成功连接到CATIA！")
    
    # 获取文档集合
    documents = caa.documents
    print("成功获取文档集合")
    
    # 列出CATIA文件
    catia_files = list_catia_files(directory)
    print(f"\n找到 {len(catia_files)} 个CATIA文件：")
    for i, file in enumerate(catia_files, 1):
        full_path = os.path.join(directory, file)
        size = get_file_info(full_path)
        print(f"{i}. {file} ({size})")
    
    # 让用户选择要打开的文件
    if catia_files:
        while True:
            print("\n请选择要打开的文件编号（1-{0}），输入0退出：".format(len(catia_files)))
            choice = input().strip()
            
            if choice == '0':
                print("程序退出")
                break
                
            try:
                choice = int(choice)
                if 1 <= choice <= len(catia_files):
                    file = catia_files[choice - 1]
                    full_path = os.path.join(directory, file)
                    print(f"\n正在打开文件: {file}")
                    print("这可能需要一些时间，请耐心等待...")
                    
                    try:
                        # 尝试打开文件
                        start_time = time.time()
                        doc = documents.open(full_path)
                        end_time = time.time()
                        print(f"成功打开文件: {file}")
                        print(f"耗时: {end_time - start_time:.2f} 秒")
                        
                        # 询问是否关闭文件
                        print("\n是否要关闭该文件？(y/n)")
                        if input().lower().strip() == 'y':
                            doc.close()
                            print("文件已关闭")
                    except Exception as e:
                        print(f"打开文件时出错: {str(e)}")
                else:
                    print(f"请输入1到{len(catia_files)}之间的数字！")
            except ValueError:
                print("请输入有效的数字！")
    else:
        print("目录中没有找到CATIA文件！")

except Exception as e:
    print(f"发生错误: {str(e)}")
    import traceback
    print("\n详细错误信息:")
    print(traceback.format_exc()) 