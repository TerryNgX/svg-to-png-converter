import os
# 添加 Cairo DLL 目录到 PATH（可选保险：如果 DLL 加载问题复发时有用；你的实际路径）
os.environ['PATH'] = r'D:\anaconda_environment\envs\api\Library\bin;' + os.environ['PATH']

import glob
from cairosvg import svg2png

# 指定包含SVG文件的输入文件夹路径（修改为你的实际路径）
input_folder = './input_svg'  # 输入文件夹

# 指定输出PNG文件的文件夹路径（如果为空，则与输入文件夹相同）
output_folder = './output_png'  # 输出文件夹（可选，如果不需要单独文件夹，设为 input_folder）

# PNG 输出尺寸（可选：如果不指定，则使用SVG默认尺寸；单位：像素）
output_width = 512  # 示例宽度，设为 None 以忽略
output_height = 512  # 示例高度，设为 None 以忽略

# 如果输出文件夹不存在，则创建它
if output_folder and not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 获取文件夹中所有SVG文件
svg_files = glob.glob(os.path.join(input_folder, '*.svg'))

if not svg_files:
    print("输入文件夹中未找到SVG文件！")
else:
    print(f"找到 {len(svg_files)} 个SVG文件，开始转换...")

    for svg_file in svg_files:
        # 获取原文件名（不含扩展名）
        original_name = os.path.splitext(os.path.basename(svg_file))[0]

        # 生成对应的PNG文件名（使用原名称）
        png_filename = original_name + '.png'

        # 输出路径
        if output_folder:
            png_file = os.path.join(output_folder, png_filename)
        else:
            png_file = os.path.join(input_folder, png_filename)

        try:
            # 转换SVG到PNG（添加尺寸参数，如果指定）
            kwargs = {}
            if output_width is not None:
                kwargs['output_width'] = output_width
            if output_height is not None:
                kwargs['output_height'] = output_height
            svg2png(url=svg_file, write_to=png_file, **kwargs)
            print(f"转换成功: {os.path.basename(svg_file)} -> {png_filename}")
        except Exception as e:
            print(f"转换失败 {os.path.basename(svg_file)}: {str(e)}")

    print("所有转换完成！")
