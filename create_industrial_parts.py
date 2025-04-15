#!/usr/bin/python3.9

"""
创建六个常见工业零件的示例程序

包括：
1. 圆柱轴
2. 法兰盘
3. 齿轮
4. 螺栓
5. 螺母
6. 轴承座

要求：
- CATIA必须运行
"""

from pycatia import catia
from pycatia.mec_mod_interfaces.part_document import PartDocument
from math import pi, cos, sin

class IndustrialPartCreator:
    def __init__(self):
        self.caa = catia()
        self.documents = self.caa.documents
        
    def create_cylinder_shaft(self):
        """创建圆柱轴"""
        part_document: PartDocument = self.documents.add("Part")
        part = part_document.part
        
        # 创建主体
        body = part.main_body
        part.in_work_object = body
        
        # 创建草图
        sketches = body.sketches
        xy_plane = part.origin_elements.plane_xy
        sketch = sketches.add(part.create_reference_from_object(xy_plane))
        
        # 打开草图编辑
        factory_2d = sketch.open_edition()
        # 创建圆
        circle = factory_2d.create_closed_circle(0, 0, 20)  # 半径20mm
        sketch.close_edition()
        
        # 拉伸
        shape_factory = part.shape_factory
        pad = shape_factory.add_new_pad(sketch, 100)  # 长度100mm
        
        part.update()
        # 保存文件
        part_document.save_as("D:\\ps-cad-agent\\pycatia\\cylinder_shaft.CATPart")
        return part_document
        
    def create_flange(self):
        """创建法兰盘"""
        part_document: PartDocument = self.documents.add("Part")
        part = part_document.part
        
        body = part.main_body
        part.in_work_object = body
        
        # 创建基础圆盘
        sketches = body.sketches
        xy_plane = part.origin_elements.plane_xy
        sketch = sketches.add(part.create_reference_from_object(xy_plane))
        
        factory_2d = sketch.open_edition()
        # 创建外圆和内圆
        outer_circle = factory_2d.create_closed_circle(0, 0, 50)  # 外径100mm
        inner_circle = factory_2d.create_closed_circle(0, 0, 15)  # 内径30mm
        sketch.close_edition()
        
        shape_factory = part.shape_factory
        pad = shape_factory.add_new_pad(sketch, 10)  # 厚度10mm
        
        # 创建螺栓孔
        hole_sketch = sketches.add(part.create_reference_from_object(xy_plane))
        factory_2d = hole_sketch.open_edition()
        
        # 创建4个等分布的孔
        for i in range(4):
            angle = i * pi / 2
            x = 35 * cos(angle)
            y = 35 * sin(angle)
            hole = factory_2d.create_closed_circle(x, y, 5)  # 孔径10mm
            
        hole_sketch.close_edition()
        
        # 拉伸切除
        pocket = shape_factory.add_new_pocket(hole_sketch, 10)
        
        part.update()
        # 保存文件
        part_document.save_as("D:\\ps-cad-agent\\pycatia\\flange.CATPart")
        return part_document
        
    def create_gear(self):
        """创建简单齿轮"""
        part_document: PartDocument = self.documents.add("Part")
        part = part_document.part
        
        body = part.main_body
        part.in_work_object = body
        
        # 创建基础圆盘
        sketches = body.sketches
        xy_plane = part.origin_elements.plane_xy
        sketch = sketches.add(part.create_reference_from_object(xy_plane))
        
        factory_2d = sketch.open_edition()
        # 创建基圆和轴孔
        outer_circle = factory_2d.create_closed_circle(0, 0, 40)  # 基圆直径80mm
        inner_circle = factory_2d.create_closed_circle(0, 0, 10)  # 轴孔直径20mm
        sketch.close_edition()
        
        shape_factory = part.shape_factory
        pad = shape_factory.add_new_pad(sketch, 20)  # 厚度20mm
        
        part.update()
        # 保存文件
        part_document.save_as("D:\\ps-cad-agent\\pycatia\\gear.CATPart")
        return part_document
        
    def create_bolt(self):
        """创建螺栓"""
        part_document: PartDocument = self.documents.add("Part")
        part = part_document.part
        
        body = part.main_body
        part.in_work_object = body
        
        # 创建螺栓头
        sketches = body.sketches
        xy_plane = part.origin_elements.plane_xy
        head_sketch = sketches.add(part.create_reference_from_object(xy_plane))
        
        factory_2d = head_sketch.open_edition()
        # 创建六角形
        radius = 10  # 六角头外接圆半径
        for i in range(6):
            angle1 = i * pi / 3
            angle2 = (i + 1) * pi / 3
            x1 = radius * cos(angle1)
            y1 = radius * sin(angle1)
            x2 = radius * cos(angle2)
            y2 = radius * sin(angle2)
            if i == 0:
                first_point = factory_2d.create_point(x1, y1)
            line = factory_2d.create_line(x1, y1, x2, y2)
            
        head_sketch.close_edition()
        
        shape_factory = part.shape_factory
        head = shape_factory.add_new_pad(head_sketch, 8)  # 头部高度8mm
        
        # 创建螺杆
        shaft_sketch = sketches.add(part.create_reference_from_object(xy_plane))
        factory_2d = shaft_sketch.open_edition()
        circle = factory_2d.create_closed_circle(0, 0, 6)  # 螺杆直径12mm
        shaft_sketch.close_edition()
        
        shaft = shape_factory.add_new_pad(shaft_sketch, 30)  # 螺杆长度30mm
        
        part.update()
        # 保存文件
        part_document.save_as("D:\\ps-cad-agent\\pycatia\\bolt.CATPart")
        return part_document
        
    def create_nut(self):
        """创建螺母"""
        part_document: PartDocument = self.documents.add("Part")
        part = part_document.part
        
        body = part.main_body
        part.in_work_object = body
        
        # 创建六角体
        sketches = body.sketches
        xy_plane = part.origin_elements.plane_xy
        sketch = sketches.add(part.create_reference_from_object(xy_plane))
        
        factory_2d = sketch.open_edition()
        # 创建六角形
        radius = 10  # 六角形外接圆半径
        for i in range(6):
            angle1 = i * pi / 3
            angle2 = (i + 1) * pi / 3
            x1 = radius * cos(angle1)
            y1 = radius * sin(angle1)
            x2 = radius * cos(angle2)
            y2 = radius * sin(angle2)
            if i == 0:
                first_point = factory_2d.create_point(x1, y1)
            line = factory_2d.create_line(x1, y1, x2, y2)
            
        sketch.close_edition()
        
        shape_factory = part.shape_factory
        body = shape_factory.add_new_pad(sketch, 8)  # 高度8mm
        
        # 创建中心孔
        hole_sketch = sketches.add(part.create_reference_from_object(xy_plane))
        factory_2d = hole_sketch.open_edition()
        hole = factory_2d.create_closed_circle(0, 0, 6)  # 孔径12mm
        hole_sketch.close_edition()
        
        pocket = shape_factory.add_new_pocket(hole_sketch, 8)
        
        part.update()
        # 保存文件
        part_document.save_as("D:\\ps-cad-agent\\pycatia\\nut.CATPart")
        return part_document
        
    def create_bearing_housing(self):
        """创建轴承座"""
        part_document: PartDocument = self.documents.add("Part")
        part = part_document.part
        
        body = part.main_body
        part.in_work_object = body
        
        # 创建底座
        sketches = body.sketches
        xy_plane = part.origin_elements.plane_xy
        base_sketch = sketches.add(part.create_reference_from_object(xy_plane))
        
        factory_2d = base_sketch.open_edition()
        # 创建矩形底座
        factory_2d.create_line(-40, -30, 40, -30)
        factory_2d.create_line(40, -30, 40, 30)
        factory_2d.create_line(40, 30, -40, 30)
        factory_2d.create_line(-40, 30, -40, -30)
        base_sketch.close_edition()
        
        shape_factory = part.shape_factory
        base = shape_factory.add_new_pad(base_sketch, 10)  # 底座高度10mm
        
        # 创建轴承座主体
        body_sketch = sketches.add(part.create_reference_from_object(xy_plane))
        factory_2d = body_sketch.open_edition()
        outer_circle = factory_2d.create_closed_circle(0, 0, 25)  # 外径50mm
        body_sketch.close_edition()
        
        body = shape_factory.add_new_pad(body_sketch, 40)  # 高度40mm
        
        # 创建轴承孔
        hole_sketch = sketches.add(part.create_reference_from_object(xy_plane))
        factory_2d = hole_sketch.open_edition()
        hole = factory_2d.create_closed_circle(0, 0, 20)  # 孔径40mm
        hole_sketch.close_edition()
        
        pocket = shape_factory.add_new_pocket(hole_sketch, 40)
        
        # 创建安装孔
        mount_sketch = sketches.add(part.create_reference_from_object(xy_plane))
        factory_2d = mount_sketch.open_edition()
        # 创建4个安装孔
        mount_holes = [
            (-30, -20),
            (-30, 20),
            (30, -20),
            (30, 20)
        ]
        for x, y in mount_holes:
            hole = factory_2d.create_closed_circle(x, y, 5)  # 孔径10mm
            
        mount_sketch.close_edition()
        
        pocket = shape_factory.add_new_pocket(mount_sketch, 10)
        
        part.update()
        # 保存文件
        part_document.save_as("D:\\ps-cad-agent\\pycatia\\bearing_housing.CATPart")
        return part_document

def main():
    creator = IndustrialPartCreator()
    
    # 创建所有零件
    creator.create_cylinder_shaft()
    creator.create_flange()
    creator.create_gear()
    creator.create_bolt()
    creator.create_nut()
    creator.create_bearing_housing()
    
if __name__ == "__main__":
    main() 