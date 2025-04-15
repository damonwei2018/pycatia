from pycatia import catia
import math
import time
from pycatia.enumeration.enumeration_types import cat_work_mode_type

class AssemblyExploder:
    def __init__(self):
        # 连接到CATIA
        self.caa = catia()
        print("成功连接到CATIA！")
        
        # 获取当前活动文档
        self.doc = self.caa.active_document
        if not self.doc:
            raise Exception("没有打开的文档！")
        print("成功获取活动文档")
        
        # 获取产品
        self.product = self.doc.product
        
        # 切换到设计模式
        self.product.apply_work_mode(cat_work_mode_type.index("DESIGN_MODE"))
        print("切换到设计模式")
        
        # 获取活动窗口和视图
        self.active_window = self.caa.active_window
        self.active_viewer = self.active_window.active_viewer
        self.view_3d = self.active_viewer.create_viewer_3d()
        self.viewpoint_3d = self.view_3d.viewpoint_3d
        print("成功获取3D视图控制器")
        
    def get_all_products(self):
        """获取所有子产品"""
        products = []
        
        def collect_products(product):
            # 激活所有终端节点
            product.activate_default_shape()
            
            # 收集直接子产品
            for child in product.products:
                products.append(child)
                collect_products(child)
        
        collect_products(self.product)
        return products
    
    def calculate_grid(self, count):
        """计算网格大小"""
        # 计算最接近的正方形网格
        grid_size = math.ceil(math.sqrt(count))
        return grid_size, grid_size
    
    def move_product(self, product, x, y, z, rotation_angle=0):
        """移动并旋转产品"""
        try:
            # 创建变换矩阵（包含旋转和平移）
            cos_angle = math.cos(math.radians(rotation_angle))
            sin_angle = math.sin(math.radians(rotation_angle))
            
            transformation = (
                cos_angle, -sin_angle, 0.0,  # 旋转矩阵的第一行
                sin_angle, cos_angle, 0.0,   # 旋转矩阵的第二行
                0.0, 0.0, 1.0,               # 旋转矩阵的第三行
                x, y, z                      # 平移向量
            )
            
            # 应用变换
            product.move.apply(transformation)
            return True
        except Exception as e:
            print(f"移动部件 {product.name} 时出错: {str(e)}")
            return False
    
    def animate_assembly(self, duration=180):  # 180秒 = 3分钟
        """动画展开装配体"""
        print("开始动画...")
        
        # 获取所有产品
        products = self.get_all_products()
        print(f"找到{len(products)}个部件")
        
        # 计算网格
        rows, cols = self.calculate_grid(len(products))
        print(f"使用 {rows}x{cols} 网格布局")
        
        start_time = time.time()
        rotation_speed = 720 / duration  # 720度/总时间
        
        while time.time() - start_time < duration:
            current_time = time.time() - start_time
            
            # 计算当前间距（200-600-200的循环）
            phase = (current_time % 30) / 30  # 每30秒一个循环
            if phase < 0.5:
                # 0-0.5：从200到600
                spacing = 200 + 800 * phase
            else:
                # 0.5-1：从600到200
                spacing = 600 - 800 * (phase - 0.5)
            
            # 计算当前旋转角度
            current_rotation = rotation_speed * current_time
            
            # 计算起始位置
            start_x = -(cols * spacing) / 2
            start_y = -(rows * spacing) / 2
            
            # 更新所有产品的位置和旋转
            for i, product in enumerate(products):
                # 计算网格位置
                row = i // cols
                col = i % cols
                
                # 计算目标位置
                x = start_x + (col * spacing)
                y = start_y + (row * spacing)
                z = 0
                
                # 移动并旋转产品
                self.move_product(product, x, y, z, current_rotation)
            
            # 更新视图
            self.active_viewer.update()
            self.active_viewer.reframe()
            
            # 控制动画帧率
            time.sleep(0.05)
            
            # 打印进度
            if int(current_time) % 10 == 0:  # 每10秒打印一次进度
                print(f"进度: {int(current_time/duration*100)}%, 当前间距: {spacing:.1f}, 旋转角度: {current_rotation:.1f}度")
        
        print("动画完成")
    
    def set_isometric_view(self):
        """设置等轴测视图"""
        try:
            # 设置等轴测视图方向
            self.viewpoint_3d.put_sight_direction((0.577, 0.577, 0.577))
            self.active_viewer.update()
            self.active_viewer.reframe()
            print("设置等轴测视图")
        except Exception as e:
            print(f"设置视图时出错: {str(e)}")

def run_animation():
    try:
        exploder = AssemblyExploder()
        
        # 设置等轴测视图
        exploder.set_isometric_view()
        
        # 运行动画
        exploder.animate_assembly(duration=180)  # 3分钟
        
        print("操作完成！")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        import traceback
        print("\n详细错误信息:")
        print(traceback.format_exc())

if __name__ == "__main__":
    run_animation() 