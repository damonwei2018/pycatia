from pycatia import catia
from pycatia.mec_mod_interfaces.part_document import PartDocument
from pycatia.enumeration.enumeration_types import cat_work_mode_type

def analyze_feature_tree():
    # 连接到CATIA
    caa = catia()
    part_document: PartDocument = caa.active_document
    part = part_document.part
    
    print(f"\n当前文档: {part_document.name}")
    
    # 获取所有实体
    bodies = part.bodies
    print(f"\n实体数量: {bodies.count}")
    
    # 分析每个实体
    for body in bodies:
        print(f"\n实体名称: {body.name}")
        
        # 获取实体的属性
        try:
            reference = part.create_reference_from_object(body)
            spa_workbench = part_document.spa_workbench()
            measurable = spa_workbench.get_measurable(reference)
            
            # 获取基本属性
            print(f"体积: {measurable.volume}")
            print(f"表面积: {measurable.area}")
            print(f"重心: {measurable.get_cog()}")
            
            # 获取惯性属性
            inertia = spa_workbench.inertias.add(body)
            print(f"质量: {inertia.mass}")
            print(f"密度: {inertia.density}")
        except Exception as e:
            print(f"获取属性时出错: {str(e)}")
        
        # 获取参数
        try:
            parameters = part.parameters
            root_parameter_set = parameters.root_parameter_set
            parameter_sets = root_parameter_set.parameter_sets
            
            print("\n参数:")
            for param_set in parameter_sets:
                print(f"\n参数集: {param_set.name}")
                sub_params = param_set.all_parameters
                for param in sub_params:
                    try:
                        print(f"    {param.name} = {param.value}")
                    except:
                        pass
        except Exception as e:
            print(f"获取参数时出错: {str(e)}")
            
        # 获取特征
        selection = part_document.selection
        selection.clear()
        
        # 尝试不同类型的特征
        feature_types = [
            "Sketch",
            "Pad",
            "Pocket",
            "Shaft",
            "Groove",
            "Hole"
        ]
        
        print("\n特征:")
        for feature_type in feature_types:
            try:
                selection.search(f"{feature_type}.*, all")
                if selection.count > 0:
                    print(f"\n{feature_type}特征数量: {selection.count}")
                    for i in range(selection.count):
                        feature = selection.item2(i + 1).value
                        print(f"    名称: {feature.name}")
            except:
                continue
            finally:
                selection.clear()

if __name__ == "__main__":
    analyze_feature_tree() 