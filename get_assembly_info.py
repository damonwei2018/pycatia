from pycatia import catia
import json
import os
from datetime import datetime

def safe_get_attr(obj, attr_name):
    """安全地获取属性值"""
    try:
        value = getattr(obj, attr_name, None)
        if callable(value):
            try:
                result = value()
                if isinstance(result, (str, int, float, bool, type(None))):
                    return result
                return str(result)
            except:
                return None
        if isinstance(value, (str, int, float, bool, type(None))):
            return value
        return str(value)
    except:
        return None

def get_geometric_elements(part):
    """获取几何元素信息"""
    try:
        elements = []
        # 获取主体
        if hasattr(part, 'bodies'):
            for body in part.bodies:
                body_info = {
                    "name": safe_get_attr(body, 'name'),
                    "features": [],
                    "sketches": []
                }
                
                # 获取特征
                if hasattr(body, 'features'):
                    for feature in body.features:
                        feature_info = {
                            "name": safe_get_attr(feature, 'name'),
                            "type": safe_get_attr(feature, 'type_name')
                        }
                        body_info["features"].append(feature_info)
                
                # 获取草图
                if hasattr(body, 'sketches'):
                    for sketch in body.sketches:
                        sketch_info = {
                            "name": safe_get_attr(sketch, 'name'),
                            "type": safe_get_attr(sketch, 'type_name')
                        }
                        body_info["sketches"].append(sketch_info)
                
                elements.append(body_info)
        return elements
    except Exception as e:
        print(f"获取几何元素时出错: {str(e)}")
        return []

def get_constraints_info(product):
    """获取约束信息"""
    try:
        constraints = []
        if hasattr(product, 'constraints'):
            constraints_collection = product.constraints
            if hasattr(constraints_collection, 'item'):
                for i in range(constraints_collection.count):
                    try:
                        constraint = constraints_collection.item(i+1)
                        constraint_info = {
                            "name": safe_get_attr(constraint, 'name'),
                            "type": safe_get_attr(constraint, 'constraint_type'),
                            "status": safe_get_attr(constraint, 'status'),
                            "locked": safe_get_attr(constraint, 'is_locked')
                        }
                        constraints.append(constraint_info)
                    except Exception as e:
                        print(f"获取第{i+1}个约束时出错: {str(e)}")
        return constraints
    except Exception as e:
        print(f"获取约束信息时出错: {str(e)}")
        return []

def get_material_info(part):
    """获取材料信息"""
    try:
        if hasattr(part, 'material'):
            material = part.material
            return {
                "name": safe_get_attr(material, 'name'),
                "description": safe_get_attr(material, 'description'),
                "density": safe_get_attr(material, 'density'),
                "young_modulus": safe_get_attr(material, 'young_modulus'),
                "poisson_ratio": safe_get_attr(material, 'poisson_ratio')
            }
    except Exception as e:
        print(f"获取材料信息时出错: {str(e)}")
        return None

def get_parameters(obj):
    """获取参数信息"""
    try:
        params = []
        if hasattr(obj, 'parameters'):
            for param in obj.parameters:
                param_info = {
                    "name": safe_get_attr(param, 'name'),
                    "value": safe_get_attr(param, 'value'),
                    "type": safe_get_attr(param, 'value_type'),
                    "formula": safe_get_attr(param, 'formula'),
                    "unit": safe_get_attr(param, 'unit')
                }
                params.append(param_info)
        return params
    except Exception as e:
        print(f"获取参数信息时出错: {str(e)}")
        return []

def get_part_info(part):
    """获取零件信息"""
    try:
        info = {
            "name": safe_get_attr(part, 'name'),
            "parameters": get_parameters(part),
            "material": get_material_info(part),
            "geometric_elements": get_geometric_elements(part),
            "properties": {
                "mass": safe_get_attr(part, 'mass'),
                "volume": safe_get_attr(part, 'volume'),
                "density": safe_get_attr(part, 'density'),
                "area": safe_get_attr(part, 'area'),
                "gravity_center": safe_get_attr(part, 'gravity_center')
            }
        }
        return info
    except Exception as e:
        print(f"获取零件信息时出错: {str(e)}")
        return None

def get_product_info(product):
    """获取产品信息"""
    try:
        info = {
            "name": safe_get_attr(product, 'name'),
            "part_number": safe_get_attr(product, 'part_number'),
            "description": safe_get_attr(product, 'description'),
            "revision": safe_get_attr(product, 'revision'),
            "nomenclature": safe_get_attr(product, 'nomenclature'),
            "definition": safe_get_attr(product, 'definition'),
            "parameters": get_parameters(product),
            "constraints": get_constraints_info(product),
            "properties": {
                "mass": safe_get_attr(product, 'mass'),
                "volume": safe_get_attr(product, 'volume'),
                "density": safe_get_attr(product, 'density'),
                "area": safe_get_attr(product, 'area'),
                "gravity_center": safe_get_attr(product, 'gravity_center')
            },
            "children": []
        }
        
        # 获取零件信息（如果是零件）
        if hasattr(product, 'part'):
            info["part"] = get_part_info(product.part)
        
        # 获取子产品信息
        try:
            products = getattr(product, 'products', [])
            if products and not callable(products):
                print(f"处理产品 {info['name']} 的子组件...")
                info["products_count"] = len(products)
                for child in products:
                    child_info = get_product_info(child)
                    if child_info:
                        info["children"].append(child_info)
        except Exception as e:
            print(f"处理子产品时出错: {str(e)}")
        
        return info
    except Exception as e:
        print(f"获取产品信息时出错: {str(e)}")
        return None

def get_document_info(doc):
    """获取文档信息"""
    try:
        info = {
            "name": safe_get_attr(doc, 'name'),
            "full_name": safe_get_attr(doc, 'full_name'),
            "path": safe_get_attr(doc, 'path'),
            "parameters": get_parameters(doc),
            "product": None
        }
        
        # 获取产品信息
        try:
            product = getattr(doc, 'product', None)
            if product and not callable(product):
                print("获取产品信息...")
                info["product"] = get_product_info(product)
        except Exception as e:
            print(f"获取产品信息时出错: {str(e)}")
        
        return info
    except Exception as e:
        print(f"获取文档信息时出错: {str(e)}")
        return None

try:
    # 连接到CATIA
    caa = catia()
    print("成功连接到CATIA！")
    
    # 获取当前活动文档
    active_doc = caa.active_document
    if not active_doc:
        print("没有打开的文档！")
        exit()
    
    print(f"正在分析文档: {safe_get_attr(active_doc, 'name')}")
    
    # 获取所有信息
    info = {
        "timestamp": datetime.now().isoformat(),
        "document": get_document_info(active_doc)
    }
    
    # 保存为JSON文件
    output_file = "assembly_info.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    
    print(f"\n信息已保存到: {output_file}")
    
except Exception as e:
    print(f"发生错误: {str(e)}")
    import traceback
    print("\n详细错误信息:")
    print(traceback.format_exc()) 