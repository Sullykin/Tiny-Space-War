from cx_Freeze import setup, Executable 

buildOptions = dict(include_files = ['C:/Users/Connor/Documents/CF1/Python/Projects/Completed/Tiny Space War/Assets/']) #folder,relative path. Use tuple like in the single file to set a absolute path.

setup(
         name = "Tiny Space War",
         version = "1.2.1",
         description = "description",
         options = dict(build_exe = buildOptions),
         executables = [Executable("Tiny Space War.py")])
