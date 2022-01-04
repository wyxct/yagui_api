import os
import shutil
from src import version

package_name = "manage"

def removepath(path):  # 传入存储的list
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path): 
            if file == '__pycache__':
                shutil.rmtree(file_path)
                print("remove: "+file_path)
            else:
               removepath(file_path) 
        else:
            pass
    
def package_program():
    print("manage server start package")
    if os.path.exists("manage"):
        print("remove manage dir")
        shutil.rmtree('manage')
        print("remove manage dir successfully")
    os.system("pyinstaller manage.py  --distpath ./  -y --clean")
    os.system("apidoc -i src/ -o static/ -S")
    #shutil.move("dist/main.exe", "dist/server.exe")
    print("compile file successfully")

    print("copy apidoc template")
    shutil.copytree("template","manage/template")
    print("copy config file")
    shutil.copytree("src", "manage/src")
    print("copy static file")
    shutil.copytree("static", "manage/static")
    print("copy templates file")
    shutil.copytree("templates", "manage/templates")
    print("copy scripts file")
    shutil.copytree("scripts", "manage/scripts")
    removepath('manage/src')
    print("tar file")
    tar_filename = f"TaskDispacher_{version}"
    shutil.make_archive(tar_filename, "zip", "manage")
    print("tar file successfully")
    print("package monitor server successfully")


if __name__ == '__main__':
    package_program()
