from pycatia import catia

try:
    # 尝试连接CATIA
    caa = catia()
    print("成功连接到CATIA！")
except Exception as e:
    print(f"连接失败: {str(e)}") 