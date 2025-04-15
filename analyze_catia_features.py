#!/usr/bin/python3.9

"""
示例 - CATIA特征树分析
描述：
    分析当前打开的CATIA文档中的特征树，并导出为JSON文件
    导出文件名将与CAD文件同名，但扩展名为.json

要求：
    - CATIA必须运行
    - 必须有打开的文档
"""

import os
import json
from pycatia import catia
from pycatia.mec_mod_interfaces.part_document import PartDocument
from pycatia.enumeration.enumeration_types import cat_measurable_name
from pycatia.enumeration.enumeration_types import geometrical_feature_type

def analyze_features():
    try:
        # 连接到CATIA
        caa = catia()
        print("已连接到CATIA\n")
        
        # 获取当前文档
        part_document: PartDocument = caa.active_document
        if not part_document:
            print("错误：未找到活动文档")
            return
            
        print(f"分析文档: {os.path.basename(part_document.full_name)}")
        
        # 获取零件对象
        part = part_document.part
        selection = part_document.selection
        selection.clear()
        
        # 初始化特征树数据
        feature_tree = {
            "document_name": os.path.basename(part_document.full_name),
            "bodies": [],
            "features": [],
            "parameters": [],
            "relations": []
        }
        
        # 分析实体
        try:
            bodies = part.bodies
            for body in bodies:
                body_data = {
                    "name": body.name,
                    "features": []
                }
                
                # 获取实体特征
                try:
                    # 清除之前的选择
                    selection.clear()
                    # 搜索该实体中的所有特征
                    selection.search(f"'Part Design'.*, sel")
                    selection.add(body)
                    
                    for i in range(selection.count):
                        feature = selection.item2(i + 1).value
                        try:
                            feature_data = {
                                "name": feature.name,
                                "type": str(type(feature).__name__)
                            }
                            
                            # 获取特征参考
                            try:
                                reference = part.create_reference_from_object(feature)
                                spa_workbench = part_document.spa_workbench()
                                measurable = spa_workbench.get_measurable(reference)
                                
                                # 获取几何类型
                                try:
                                    geom_type = measurable.geometry_name
                                    feature_data["geometry_type"] = cat_measurable_name[geom_type]
                                except:
                                    pass
                                    
                                # 尝试获取特征的几何属性
                                try:
                                    feature_data["properties"] = {
                                        "volume": measurable.volume,
                                        "area": measurable.area
                                    }
                                except:
                                    pass
                                    
                            except Exception as e:
                                print(f"获取特征 {feature.name} 的参考时出错：{str(e)}")
                                
                            body_data["features"].append(feature_data)
                        except Exception as e:
                            print(f"处理特征时出错：{str(e)}")
                            
                    selection.clear()
                except Exception as e:
                    print(f"搜索特征时出错：{str(e)}")
                    
                # 获取实体属性
                try:
                    reference = part.create_reference_from_object(body)
                    spa_workbench = part_document.spa_workbench()
                    measurable = spa_workbench.get_measurable(reference)
                    
                    # 获取基本属性
                    body_data["properties"] = {
                        "volume": measurable.volume,
                        "area": measurable.area,
                        "center_of_gravity": measurable.get_cog()
                    }
                    
                    # 获取惯性属性
                    inertia = spa_workbench.inertias.add(body)
                    body_data["properties"].update({
                        "mass": inertia.mass,
                        "density": inertia.density
                    })
                    
                except Exception as e:
                    print(f"获取实体属性时出错：{str(e)}")
                    
                feature_tree["bodies"].append(body_data)
        except Exception as e:
            print(f"获取实体时出错：{str(e)}")
            
        # 分析参数
        try:
            parameters = part.parameters
            root_parameter_set = parameters.root_parameter_set
            parameter_sets = root_parameter_set.parameter_sets
            
            for param_set in parameter_sets:
                try:
                    params = param_set.all_parameters
                    for param in params:
                        param_data = {
                            "name": param.name,
                            "type": str(type(param).__name__),
                            "value": str(param.valuate()),
                            "parameter_set": param_set.name
                        }
                        feature_tree["parameters"].append(param_data)
                except Exception as e:
                    print(f"处理参数集 {param_set.name} 时出错：{str(e)}")
        except Exception as e:
            print(f"获取参数时出错：{str(e)}")
            
        # 分析关系
        try:
            relations = part.relations
            for relation in relations:
                try:
                    relation_data = {
                        "name": relation.name,
                        "type": str(type(relation).__name__),
                        "expression": relation.expression
                    }
                    feature_tree["relations"].append(relation_data)
                except Exception as e:
                    print(f"处理关系 {relation.name} 时出错：{str(e)}")
        except Exception as e:
            print(f"获取关系时出错：{str(e)}")
            
        # 生成输出文件名
        base_name = os.path.splitext(os.path.basename(part_document.full_name))[0]
        output_file = f"{base_name}_features.json"
        
        # 保存到JSON文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(feature_tree, f, ensure_ascii=False, indent=4)
            
        print(f"\n特征树已导出到: {output_file}")
        
    except Exception as e:
        print(f"程序执行出错：{str(e)}")

if __name__ == "__main__":
    analyze_features() 