from pycatia import catia
import math
import time

class SceneAnimator:
    def __init__(self):
        # 连接到CATIA
        self.caa = catia()
        print("成功连接到CATIA！")
        
        # 获取当前活动文档
        self.doc = self.caa.active_document
        if not self.doc:
            raise Exception("没有打开的文档！")
        print("成功获取活动文档")
        
        # 获取活动窗口和视图
        self.active_window = self.caa.active_window
        self.active_viewer = self.active_window.active_viewer
        self.view_3d = self.active_viewer.create_viewer_3d()
        self.viewpoint_3d = self.view_3d.viewpoint_3d
        print("成功获取3D视图控制器")
        
    def rotate_view(self, angle):
        """旋转视图"""
        try:
            # 计算新的视点方向
            x = math.cos(angle)
            z = math.sin(angle)
            y = 0.5  # 保持一定的俯视角度
            
            # 设置视点方向
            self.viewpoint_3d.put_sight_direction((x, y, z))
            
            # 更新视图
            self.active_viewer.update()
            # 自动调整视图以适应所有内容
            self.active_viewer.reframe()
            print(f"旋转到角度: {math.degrees(angle):.1f}度")
            
        except Exception as e:
            print(f"旋转出错: {str(e)}")
        
    def simple_rotation(self, duration=10, total_rotations=2):
        """简单的旋转动画
        
        Args:
            duration: 动画持续时间（秒）
            total_rotations: 总旋转圈数
        """
        print("开始旋转动画...")
        start_time = time.time()
        
        # 计算总角度和角速度
        total_angle = total_rotations * 2 * math.pi
        angular_speed = total_angle / duration
        
        while time.time() - start_time < duration:
            current_time = time.time() - start_time
            current_angle = angular_speed * current_time
            self.rotate_view(current_angle)
            time.sleep(0.1)  # 控制帧率

def run_animation_sequence():
    try:
        animator = SceneAnimator()
        print("开始动画序列...")
        
        # 执行旋转动画：10秒内旋转2圈
        animator.simple_rotation(duration=10, total_rotations=2)
        
        print("动画序列完成！")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        import traceback
        print("\n详细错误信息:")
        print(traceback.format_exc())

if __name__ == "__main__":
    run_animation_sequence() 