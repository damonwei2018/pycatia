from pycatia import catia
import os

try:
    # 连接到CATIA
    caa = catia()
    print("成功连接到CATIA！")
    
    # 获取文档集合
    documents = caa.documents
    print("成功获取文档集合")
    
    # 指定要打开的文件
    file_name = "YUN_100_Front_Hood_Package.CATProduct"
    file_path = os.path.join(os.getcwd(), "models", "Yun_100_Sdeven_20140716", file_name)
    
    print(f"\n正在打开文件: {file_name}")
    print("这可能需要一些时间，请耐心等待...")
    
    # 打开文件
    doc = documents.open(file_path)
    print("文件加载成功！")
    
    # 获取产品信息
    product = doc.product
    print("\n装配体信息：")
    print(f"名称: {product.name}")
    print(f"部件数量: {len(product.products)}")
    
    # 列出所有部件
    print("\n包含的部件：")
    for i, part in enumerate(product.products, 1):
        print(f"{i}. {part.name} - {part.part_number}")
        
except Exception as e:
    print(f"发生错误: {str(e)}")
    import traceback
    print("\n详细错误信息:")
    print(traceback.format_exc()) 