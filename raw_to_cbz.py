import os
import zipfile
from pathlib import Path


def create_cbz_from_folders(main_directory):
    main_dir = Path(main_directory)
    if not main_dir.is_dir():
        print(f"Error: {main_directory} is not a valid directory.")
        return
    cbz_output_path = main_dir / "CBZ_Files"
    cbz_output_path.mkdir(exist_ok=True)
    for root, dirs, files in os.walk(main_dir):
        folder_path = Path(root)
        if folder_path == cbz_output_path:
            continue
        images = sorted(
            [file for file in files if file.lower().endswith(('.jpg', '.jpeg', '.png'))]
        )
        if not images:
            print(f"No images found in {folder_path}. Skipping...")
            continue
        cbz_file_name = f"{folder_path.name}.cbz"
        cbz_file_path = cbz_output_path / cbz_file_name
        print(f"Creating CBZ file: {cbz_file_path}")
        with zipfile.ZipFile(cbz_file_path, 'w') as cbz_file:
            for image in images:
                image_path = folder_path / image
                cbz_file.write(image_path, arcname=image)
        print(f"Finished creating {cbz_file_path}")
    print("All CBZ files created successfully.")


main_directory = r"C:\Users\user\Documents\Mangas\MANGA"
create_cbz_from_folders(main_directory)
