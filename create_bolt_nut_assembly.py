from pycatia import catia
from pycatia.enumeration.enumeration_types import cat_work_mode_type
from pycatia.in_interfaces.application import Application
from pycatia.knowledge_interfaces.parameters import Parameters
import math
import os

class BoltNutCreator:
    def __init__(self):
        self.caa = catia()
        self.documents = self.caa.documents
        self.work_dir = os.path.abspath(os.path.dirname(__file__))
        
    def create_bolt(self, diameter=10, length=30):
        """创建螺栓"""
        print("开始创建螺栓...")
        
        # 创建新的零件文档
        bolt_doc = self.documents.add("Part")
        bolt_part = bolt_doc.part
        
        # 获取主要对象
        hsf = bolt_part.hybrid_shape_factory
        body = bolt_part.bodies.add()
        body.name = "Bolt"
        
        # 获取原点和平面
        xy_plane = bolt_part.origin_elements.plane_xy
        xy_plane_ref = bolt_part.create_reference_from_object(xy_plane)
        
        # 创建螺栓头
        head_height = diameter * 0.7
        head_diameter = diameter * 1.8
        
        # 创建头部圆柱
        sketches = body.sketches
        head_sketch = sketches.add(xy_plane_ref)
        
        factory2D = head_sketch.open_edition()
        head_circle = factory2D.create_closed_circle(0, 0, head_diameter/2)
        head_sketch.close_edition()
        
        # 拉伸创建头部
        shape_factory = bolt_part.shape_factory
        bolt_part.in_work_object = body
        pad = shape_factory.add_new_pad(head_sketch, head_height)
        
        # 创建螺栓杆
        shaft_sketch = sketches.add(xy_plane_ref)
        factory2D = shaft_sketch.open_edition()
        shaft_circle = factory2D.create_closed_circle(0, 0, diameter/2)
        shaft_sketch.close_edition()
        
        # 拉伸创建螺栓杆
        shaft_pad = shape_factory.add_new_pad(shaft_sketch, length)
        
        # 更新零件
        bolt_part.update()
        
        # 保存文档
        bolt_path = os.path.join(self.work_dir, "bolt.CATPart")
        if os.path.exists(bolt_path):
            os.remove(bolt_path)
        bolt_doc.save_as(bolt_path.replace("\\", "/"))
        print(f"螺栓创建完成，保存在: {bolt_path}")
        return bolt_doc
        
    def create_nut(self, diameter=10):
        """创建螺母"""
        print("开始创建螺母...")
        
        # 创建新的零件文档
        nut_doc = self.documents.add("Part")
        nut_part = nut_doc.part
        
        # 创建主体
        body = nut_part.bodies.add()
        body.name = "Nut"
        
        # 获取原点和平面
        xy_plane = nut_part.origin_elements.plane_xy
        xy_plane_ref = nut_part.create_reference_from_object(xy_plane)
        
        # 计算螺母尺寸
        nut_height = diameter * 0.8
        nut_diameter = diameter * 1.8
        
        # 创建六边形草图
        sketches = body.sketches
        nut_sketch = sketches.add(xy_plane_ref)
        
        factory2D = nut_sketch.open_edition()
        
        # 创建正六边形
        radius = nut_diameter/2
        points = []
        for i in range(6):
            angle = i * math.pi / 3
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            points.append((x, y))
        
        # 连接点形成六边形
        for i in range(6):
            factory2D.create_line(
                points[i][0], points[i][1],
                points[(i+1)%6][0], points[(i+1)%6][1]
            )
        
        nut_sketch.close_edition()
        
        # 拉伸创建螺母本体
        shape_factory = nut_part.shape_factory
        nut_part.in_work_object = body
        pad = shape_factory.add_new_pad(nut_sketch, nut_height)
        
        # 创建中心孔
        hole_sketch = sketches.add(xy_plane_ref)
        factory2D = hole_sketch.open_edition()
        hole_circle = factory2D.create_closed_circle(0, 0, diameter/2)
        hole_sketch.close_edition()
        
        # 创建通孔
        pocket = shape_factory.add_new_pocket(hole_sketch, nut_height)
        
        # 更新零件
        nut_part.update()
        
        # 保存文档
        nut_path = os.path.join(self.work_dir, "nut.CATPart")
        if os.path.exists(nut_path):
            os.remove(nut_path)
        nut_doc.save_as(nut_path.replace("\\", "/"))
        print(f"螺母创建完成，保存在: {nut_path}")
        return nut_doc
        
    def create_assembly(self):
        """创建装配体"""
        print("开始创建装配体...")
        
        # 创建新的装配体文档
        asm_doc = self.documents.add("Product")
        asm_product = asm_doc.product
        
        # 将螺栓和螺母添加到装配体
        bolt_path = os.path.join(self.work_dir, "bolt.CATPart")
        nut_path = os.path.join(self.work_dir, "nut.CATPart")
        
        products = asm_product.products
        bolt_component = products.add_component(bolt_path.replace("\\", "/"))
        nut_component = products.add_component(nut_path.replace("\\", "/"))
        
        # 移动螺母到合适位置
        nut_component.move.apply((
            1, 0, 0,
            0, 1, 0,
            0, 0, 1,
            0, 0, 15  # 沿Z轴移动到螺栓中间位置
        ))
        
        # 保存装配体
        asm_path = os.path.join(self.work_dir, "bolt_nut_assembly.CATProduct")
        if os.path.exists(asm_path):
            os.remove(asm_path)
        asm_doc.save_as(asm_path.replace("\\", "/"))
        print(f"装配体创建完成，保存在: {asm_path}")
        return asm_doc

def main():
    try:
        creator = BoltNutCreator()
        
        # 创建螺栓和螺母
        bolt_doc = creator.create_bolt()
        nut_doc = creator.create_nut()
        
        # 创建装配体
        asm_doc = creator.create_assembly()
        
        print("所有操作完成！")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        import traceback
        print("\n详细错误信息:")
        print(traceback.format_exc())

if __name__ == "__main__":
    main() 