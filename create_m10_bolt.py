from pycatia import catia
from pycatia.mec_mod_interfaces.part_document import PartDocument
import math
import os

def create_m10_bolt():
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
    body.name = "M10_Bolt"
    print("创建实体")
    
    # 获取形状工厂和混合形状工厂
    shape_factory = part.shape_factory
    hybrid_shape_factory = part.hybrid_shape_factory
    
    # 1. 创建六角头
    # 在XY平面创建草图
    sketches = body.sketches
    xy_plane = part.origin_elements.plane_xy
    head_sketch = sketches.add(part.create_reference_from_object(xy_plane))
    
    # 打开草图编辑
    factory_2d = head_sketch.open_edition()
    
    # 创建六边形（s = 17mm）
    radius = 17/2  # 六角头半宽度
    points = []
    for i in range(6):
        angle = i * math.pi / 3
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        points.append((x, y))
    
    # 连接点形成六边形
    for i in range(6):
        factory_2d.create_line(
            points[i][0], points[i][1],
            points[(i+1)%6][0], points[(i+1)%6][1]
        )
    
    # 关闭草图编辑
    head_sketch.close_edition()
    print("创建六角头草图")
    
    # 拉伸六角头（k = 6.4mm）
    part.in_work_object = body
    head_pad = shape_factory.add_new_pad(head_sketch, 6.4)
    print("拉伸六角头完成")
    
    # 2. 创建螺杆
    # 在同一平面创建圆形草图
    shaft_sketch = sketches.add(part.create_reference_from_object(xy_plane))
    factory_2d = shaft_sketch.open_edition()
    
    # 创建圆（d = 10mm）
    circle = factory_2d.create_closed_circle(0, 0, 5)  # 半径为5mm
    
    # 关闭草图编辑
    shaft_sketch.close_edition()
    print("创建螺杆草图")
    
    # 拉伸螺杆（l = 50mm）
    shaft_pad = shape_factory.add_new_pad(shaft_sketch, 50)
    print("拉伸螺杆完成")
    
    # 3. 添加倒角
    # 获取所有边
    all_edges = []
    faces = body.shapes.item(1).faces
    
    # 遍历所有面
    for i in range(faces.count):
        face = faces.item(i+1)
        edges = face.edges
        # 遍历面的所有边
        for j in range(edges.count):
            edge = edges.item(j+1)
            all_edges.append(part.create_reference_from_object(edge))
    
    # 创建1mm倒角
    try:
        chamfer = shape_factory.add_new_chamfer(all_edges, 1, 45)
        print("创建倒角完成")
    except Exception as e:
        print(f"创建倒角时出错: {str(e)}")
    
    # 4. 添加圆角
    # 在螺栓头和螺杆的过渡处添加圆角
    try:
        ref_head = part.create_reference_from_object(head_pad.shape)
        ref_shaft = part.create_reference_from_object(shaft_pad.shape)
        
        # 创建2mm圆角
        fillet = shape_factory.add_new_edge_fillet([ref_head, ref_shaft], 2)
        print("创建过渡圆角完成")
    except Exception as e:
        print(f"创建圆角时出错: {str(e)}")
    
    # 5. 创建螺纹
    try:
        # 创建螺纹的参考平面（距离螺栓头6.4mm）
        ref_xy_plane = part.create_reference_from_object(xy_plane)
        thread_plane = hybrid_shape_factory.add_new_plane_offset(
            ref_xy_plane,
            6.4,  # 偏移距离等于螺栓头高度
            False  # 反向
        )
        
        # 将平面添加到主体中
        body.append_hybrid_shape(thread_plane)
        part.update()
        
        # 获取螺杆的圆柱面
        shaft_faces = shaft_pad.shape.faces
        lateral_face = None
        
        # 查找圆柱面
        for i in range(shaft_faces.count):
            face = shaft_faces.item(i+1)
            if face.area > 1000:  # 圆柱面应该是最大的面
                lateral_face = face
                break
        
        if lateral_face:
            ref_shaft_lateral = part.create_reference_from_object(lateral_face)
            ref_thread_plane = part.create_reference_from_object(thread_plane)
            
            # 创建M10标准螺纹（螺距1.5mm）
            thread = shape_factory.add_new_thread(
                ref_shaft_lateral,  # 螺纹表面
                ref_thread_plane,   # 起始平面
                43.6,              # 长度（总长50mm减去螺栓头高度6.4mm）
                10,                # 直径
                1.5                # 螺距
            )
            print("创建螺纹完成")
        else:
            print("未找到合适的螺纹表面")
    except Exception as e:
        print(f"创建螺纹时出错: {str(e)}")
    
    # 更新零件
    part.update()
    print("创建M10螺栓完成！")
    
    return part_document

if __name__ == "__main__":
    try:
        doc = create_m10_bolt()
        # 保存文件（使用绝对路径）
        save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "M10_Bolt.CATPart"))
        # 确保路径使用正斜杠
        save_path = save_path.replace("\\", "/")
        doc.save_as(save_path)
        print(f"文件已保存为: {save_path}")
    except Exception as e:
        print(f"发生错误: {str(e)}") 