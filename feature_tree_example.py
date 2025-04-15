#! /usr/bin/python3.9

"""
示例 - 特征树操作
描述：
    1. 创建一个简单的零件（带基体和通孔）
    2. 显示特征树结构
    3. 修改特征参数

要求：
    - CATIA必须运行
"""

from pycatia import catia
from pycatia.mec_mod_interfaces.part_document import PartDocument
from pycatia.in_interfaces.specs_and_geom_window import SpecsAndGeomWindow
from pycatia.enumeration.enumeration_types import cat_specs_and_geom_window_layout

def create_and_show_features():
    # 连接到CATIA
    caa = catia()
    documents = caa.documents
    
    # 创建新零件
    part_document = documents.add("Part")
    part = part_document.part
    
    # 获取主体
    body = part.main_body
    part.in_work_object = body
    
    # 创建基础草图
    sketches = body.sketches
    xy_plane = part.origin_elements.plane_xy
    sketch = sketches.add(part.create_reference_from_object(xy_plane))
    
    # 绘制矩形
    factory_2d = sketch.open_edition()
    factory_2d.create_line(-30, -20, 30, -20)
    factory_2d.create_line(30, -20, 30, 20)
    factory_2d.create_line(30, 20, -30, 20)
    factory_2d.create_line(-30, 20, -30, -20)
    sketch.close_edition()
    
    # 拉伸特征
    shape_factory = part.shape_factory
    pad = shape_factory.add_new_pad(sketch, 40)
    pad.name = "基体"
    
    # 创建圆形草图用于切除
    hole_sketch = sketches.add(part.create_reference_from_object(xy_plane))
    factory_2d = hole_sketch.open_edition()
    factory_2d.create_closed_circle(0, 0, 10)
    hole_sketch.close_edition()
    
    # 切除特征
    pocket = shape_factory.add_new_pocket(hole_sketch, 40)
    pocket.name = "通孔"
    
    # 更新零件
    part.update()
    
    # 获取活动窗口并显示特征树
    active_window = caa.active_window
    specs_and_geom = SpecsAndGeomWindow(active_window.com_object)
    
    # 确保特征树可见
    specs_and_geom.layout = cat_specs_and_geom_window_layout.index("catWindowSpecsAndGeom")
    
    # 获取并显示参数
    parameters = part.parameters
    print("\n特征参数：")
    for param in parameters:
        try:
            print(f"参数名: {param.name}, 值: {param.value}")
        except:
            pass

if __name__ == "__main__":
    create_and_show_features() 