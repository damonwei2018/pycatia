from pycatia import catia
import os

try:
    # 连接到CATIA
    caa = catia()
    print("成功连接到CATIA！")
    
    # 获取当前活动文档
    active_doc = caa.active_document
    if not active_doc:
        print("没有打开的文档！")
        exit()
    
    # 创建输出目录
    output_dir = "web/models"
    os.makedirs(output_dir, exist_ok=True)
    
    # 导出为STL格式
    output_path = os.path.join(output_dir, "model.stl")
    print(f"正在导出模型到: {output_path}")
    
    # 执行导出
    active_doc.export_data(output_path, "stl")
    print("模型导出成功！")
    
except Exception as e:
    print(f"发生错误: {str(e)}")
    import traceback
    print("\n详细错误信息:")
    print(traceback.format_exc()) 