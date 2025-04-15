from pycatia import catia
from pycatia.mec_mod_interfaces.part_document import PartDocument

def create_simple_cylinder():
    # 连接到CATIA
    caa = catia()
    print("成功连接到CATIA！")
    
    # 创建新的零件文档
    documents = caa.documents
    part_document = documents.add("Part")
    part = part_document.part
    print("创建新的零件文档")
    
    # 创建一个新的实体
    bodies = part.bodies
    body = bodies.add()
    body.name = "SimpleCylinder"
    print("创建实体")
    
    # 获取形状工厂
    shape_factory = part.shape_factory
    
    # 在XY平面创建草图
    sketches = body.sketches
    xy_plane = part.origin_elements.plane_xy
    sketch = sketches.add(part.create_reference_from_object(xy_plane))
    
    # 打开草图编辑
    factory_2d = sketch.open_edition()
    
    # 创建圆（半径为20毫米）
    circle = factory_2d.create_closed_circle(0, 0, 20)
    
    # 关闭草图编辑
    sketch.close_edition()
    print("创建圆形草图")
    
    # 设置当前工作对象
    part.in_work_object = body
    
    # 拉伸50毫米
    pad = shape_factory.add_new_pad(sketch, 50)
    print("拉伸完成")
    
    # 更新零件
    part.update()
    print("创建圆柱体完成！")

if __name__ == "__main__":
    try:
        create_simple_cylinder()
    except Exception as e:
        print(f"发生错误: {str(e)}") 