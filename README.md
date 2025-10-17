# SVG 到 PNG 转换脚本

这是一个简单的 Python 脚本，用于批量将指定文件夹中的 SVG 文件转换为 PNG 格式。脚本使用 `cairosvg` 库进行转换，支持自定义输出尺寸和文件夹。特别适用于处理 GHS 图标或其他矢量图形。

## 功能特点
- 批量处理文件夹中的所有 `.svg` 文件。
- 保持原文件名（仅替换扩展名为 `.png`）。
- 可指定输出文件夹和 PNG 尺寸（例如 512x512 像素）。
- 错误处理：逐文件转换，失败时打印错误信息。
- Windows/Anaconda 环境兼容（包含 Cairo DLL 安装指南）。

## 要求
- Python 3.8+（推荐使用 Anaconda 或 Miniconda）。
- 依赖库：`cairosvg`（会自动安装 Cairo 相关依赖）。

## 安装
### 1. 安装 Python 环境
- 如果未安装 Anaconda，下载并安装从 [anaconda.com](https://www.anaconda.com/download)。
- 创建新环境（可选）：
  ```
  conda create -n svg_converter python=3.11
  conda activate svg_converter
  ```

### 2. 安装依赖
在激活的环境中运行：
```
conda install -c conda-forge cairo pycairo cairosvg
```
- 这会安装 Cairo 图形库及其 Python 绑定。如果你是 Windows 用户，可能会遇到 DLL 加载问题（见故障排除部分）。

### 3. Windows 特殊：安装 GTK Runtime（如果 conda 安装失败）
如果 `from cairosvg import svg2png` 导入时报 Cairo DLL 错误：
1. 下载 GTK3-Runtime（64-bit）从 [GTK Releases](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)，例如 `gtk3-runtime-3.24.35-ts-win64.exe`。
2. 运行安装器，默认路径：`C:\Program Files\GTK3-Runtime Win64`。
3. 添加到系统 PATH：
   - 右键“此电脑” > 属性 > 高级系统设置 > 环境变量 > 系统变量 > Path > 编辑 > 新建 > 输入 `C:\Program Files\GTK3-Runtime Win64\bin`。
   - 重启 CMD/PyCharm。
4. 验证：`where libcairo-2.dll` 应输出 DLL 路径。

### 4. 下载脚本
- 从 GitHub 克隆仓库：`git clone https://github.com/你的用户名/svg-to-png-converter.git`。
- 或直接下载 `svg_to_py.py` 文件。

## 使用
1. 修改脚本中的路径：
   - `input_folder = './ghs_pictograms_svg'`：SVG 输入文件夹。
   - `output_folder = './output_png'`：PNG 输出文件夹（可选）。
   - `output_width` 和 `output_height`：PNG 尺寸（设为 `None` 使用 SVG 原尺寸）。

2. 运行脚本：
   ```
   python svg_to_py.py
   ```
   示例输出：
   ```
   找到 5 个SVG文件，开始转换...
   转换成功: icon1.svg -> icon1.png
   ...
   所有转换完成！
   ```

3. 测试：将 SVG 文件放入输入文件夹，运行后检查输出文件夹。

## 故障排除
这个脚本在 Windows/Anaconda 环境中开发，常见问题是 Cairo DLL 加载失败（OSError: no library called "cairo-2"）。以下是从问题出现到完全解决的详细步骤（基于实际调试过程）：

### 问题1: 导入 `cairosvg` 时报 Cairo DLL 错误
**症状**：
```
OSError: no library called "cairo-2" was found
no library called "cairo" was found
...
cannot load library 'libcairo-2.dll': error 0x7e
```

**原因**：`cairosvg` 依赖底层 Cairo 库，但 Windows 默认未安装 DLL 文件。

**解决步骤**：
1. **激活 Anaconda 环境**：
   ```
   conda activate api  # 或你的环境名
   ```

2. **用 conda 安装 Cairo**：
   ```
   conda install -c conda-forge cairo pycairo cairosvg
   ```
   - 验证：`python -c "from cairosvg import svg2png; print('成功！')"`。
   - 如果终端成功但 PyCharm 失败：检查 PyCharm 的 Python Interpreter 设置（File > Settings > Project > Python Interpreter > 添加 Conda 环境路径，如 `D:\anaconda_environment\envs\api\python.exe`）。

3. **如果仍失败，检查 DLL**：
   ```
   dir D:\anaconda_environment\envs\api\Library\bin\libcairo-2.dll
   ```
   - 如果不存在，强制重装：
     ```
     conda uninstall --force cairo pycairo cairosvg cairocffi
     conda install -c conda-forge --force-reinstall cairo pycairo cairosvg
     ```

4. **添加临时 PATH 到脚本**（保险措施）：
   在 `svg_to_py.py` 开头添加：
   ```python
   import os
   os.environ['PATH'] = r'C:\Program Files\GTK3-Runtime Win64\bin;' + os.environ['PATH']
   ```
   - 或 Anaconda 路径：`r'D:\anaconda_environment\envs\api\Library\bin;'`。

5. **安装 GTK Runtime（最终方案）**：
   - 如“安装”部分的步骤3。
   - 重启电脑/CMD 后，运行 `where libcairo-2.dll` 验证。
   - 测试：`python -c "import cairocffi as cairo; print('Cairo 版本:', cairo.cairo_version())"`（应输出版本号）。

### 问题2: PyCharm 运行时报错，但终端正常
**原因**：PyCharm 使用了错误的 Python 解释器（例如 Microsoft Store Python）。

**解决步骤**：
1. PyCharm > File > Settings > Project > Python Interpreter > 添加 > Conda Environment > Existing > 选择 `D:\anaconda_environment\envs\api\python.exe`。
2. 重启 PyCharm，运行脚本。
3. 如果无效：Invalidate Caches (File > Invalidate Caches > Invalidate and Restart)。

### 问题3: 脚本运行但转换失败
**症状**：`转换失败: file.svg: ...`
- 检查 SVG 文件是否有效（浏览器打开测试）。
- 调整尺寸：设 `output_width = None` 以使用原尺寸。
- 权限：确保文件夹可写。

### 通用调试
- 运行简单测试：
  ```python
  try:
      from cairosvg import svg2png
      print("导入成功！")
  except Exception as e:
      print(f"错误: {e}")
  ```
- 如果 DLL 路径问题：用资源管理器搜索 `libcairo-2.dll`，手动复制到 `D:\anaconda_environment\envs\api\Library\bin`（临时）。

通过这些步骤，我从初始错误（Cairo DLL 找不到）逐步解决：先用 conda 安装，切换 PyCharm 环境，添加 PATH，最终用 GTK 确保稳定。现在脚本在 Windows 上完美运行！

## 贡献
欢迎 Pull Request！如果有 bug 或新功能建议，开 Issue 讨论。

## 许可证
MIT License - 免费使用和修改。
