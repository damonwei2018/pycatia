from pycatia import catia
import math
import time

def rotate_model(speed=1, total_time=10):
    try:
        # 连接到CATIA
        caa = catia()
        print("成功连接到CATIA！")
        
        # 获取当前活动文档
        active_doc = caa.active_document
        if not active_doc:
            print("没有打开的文档！")
            return
            
        # 获取视图窗口
        active_viewer = active_doc.active_viewer
        viewer_3d = active_viewer.viewer_3d()
        
        # 获取当前视角
        viewpoint_3d = viewer_3d.viewpoint_3d()
        
        # 执行旋转动画
        start_time = time.time()
        while time.time() - start_time < total_time:
            # 计算旋转角度（弧度）
            angle = math.radians(speed)  # 每次旋转的角度
            
            # 绕Y轴旋转
            viewpoint_3d.rotate(angle, 0, 0)
            
            # 更新视图
            viewer_3d.update()
            
            # 控制旋转速度
            time.sleep(0.01)  # 添加小延迟使旋转更平滑
            
        print("旋转完成！")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        import traceback
        print("\n详细错误信息:")
        print(traceback.format_exc())

if __name__ == "__main__":
    # 调用函数，设置旋转速度（度/帧）和总时间（秒）
    rotate_model(speed=1, total_time=10) 