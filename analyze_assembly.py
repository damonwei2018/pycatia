from pycatia import catia
from pycatia.enumeration.enumeration_types import cat_work_mode_type
from pycatia.product_structure_interfaces.product import Product

def analyze_product(product, level=0):
    """递归分析产品及其子产品"""
    indent = "  " * level
    print(f"{indent}分析产品: {product.name}")
    
    try:
        # 获取产品属性
        if hasattr(product, 'part'):
            part = product.part
            if part:
                # 激活默认形状
                shapes = part.shapes
                if shapes:
                    for shape in shapes:
                        shape.activate()
                
                # 获取并打印属性
                try:
                    mass = part.mass
                    volume = part.volume
                    wet_area = part.wet_area
                    gravity_center = part.gravity_center
                    inertia = part.inertia
                    
                    print(f"{indent}质量: {mass:.2f} kg")
                    print(f"{indent}体积: {volume:.2f} mm³")
                    print(f"{indent}表面积: {wet_area:.2f} mm²")
                    print(f"{indent}重心: X={gravity_center[0]:.2f}, Y={gravity_center[1]:.2f}, Z={gravity_center[2]:.2f}")
                    print(f"{indent}惯性矩:")
                    for i in range(3):
                        print(f"{indent}  [{inertia[i*3]:.2f}, {inertia[i*3+1]:.2f}, {inertia[i*3+2]:.2f}]")
                except Exception as e:
                    print(f"{indent}无法获取某些属性: {str(e)}")
    
    except Exception as e:
        print(f"{indent}处理产品时出错: {str(e)}")
    
    # 递归处理子产品
    if hasattr(product, 'products'):
        for child in product.products:
            analyze_product(child, level + 1)

def main():
    # 连接到 CATIA
    caa = catia()
    
    # 获取当前文档
    doc = caa.active_document
    if not doc:
        print("没有打开的文档")
        return
    
    # 确保是装配体文档
    if not hasattr(doc, 'product'):
        print("当前文档不是装配体")
        return
    
    product = doc.product
    
    # 切换到设计模式
    product.apply_work_mode(cat_work_mode_type.index("DESIGN_MODE"))
    
    # 激活所有终端节点的默认形状
    Product.activate_terminal_node(product.products)
    
    # 分析装配体
    print("开始分析装配体...")
    analyze_product(product)
    print("分析完成")

if __name__ == '__main__':
    main() 