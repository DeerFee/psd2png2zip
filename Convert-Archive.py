import os
import sys

# Добавляем путь к lib в sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(script_dir, 'lib')
sys.path.insert(0, lib_dir)

# Импортируем необходимые модули
from PIL import Image
import zipfile

def convert_psd_to_png(input_folder, output_folder):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith('.psd'):
                psd_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_folder)
                png_folder = os.path.join(output_folder, relative_path)
                os.makedirs(png_folder, exist_ok=True)
                
                png_filename = os.path.splitext(file)[0] + '.png'
                png_path = os.path.join(png_folder, png_filename)
                
                try:
                    with Image.open(psd_path) as img:
                        img.save(png_path, 'PNG')
                    print(f"Converted: {psd_path} -> {png_path}")
                except Exception as e:
                    print(f"Error converting {psd_path}: {str(e)}")

def create_zip_archives(png_folder, zip_folder):
    for root, dirs, files in os.walk(png_folder):
        if files:
            relative_path = os.path.relpath(root, png_folder)
            zip_filename = relative_path.replace(os.path.sep, '_') + '.zip'
            zip_path = os.path.join(zip_folder, zip_filename)
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, root)
                    zipf.write(file_path, arcname)
            
            print(f"Created ZIP archive: {zip_path}")

def main():
    in_folder = os.path.join(script_dir, 'in_FolderPSD')
    out_png_folder = os.path.join(script_dir, 'out_FolderPNG')
    out_zip_folder = os.path.join(script_dir, 'out_ZIP')

    os.makedirs(out_png_folder, exist_ok=True)
    os.makedirs(out_zip_folder, exist_ok=True)

    convert_psd_to_png(in_folder, out_png_folder)
    create_zip_archives(out_png_folder, out_zip_folder)

if __name__ == "__main__":
    main()