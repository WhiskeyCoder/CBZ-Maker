import os
import zipfile
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET


def create_comic_info(series_name):
    """
    Create ComicInfo.xml metadata for the manga series.
    """
    root = ET.Element("ComicInfo")
    series = ET.SubElement(root, "Series")
    series.text = series_name
    return ET.tostring(root, encoding="utf-8", method="xml").decode()


def add_metadata_to_cbz(cbz_file_path, series_name):
    """
    Add ComicInfo.xml metadata to an existing CBZ file.
    """
    metadata = create_comic_info(series_name)
    with zipfile.ZipFile(cbz_file_path, 'a') as cbz_file:
        # Add ComicInfo.xml to the CBZ file
        cbz_file.writestr("ComicInfo.xml", metadata)
    print(f"Metadata added to {cbz_file_path}")


def create_cbz_from_folders(main_directory):
    main_dir = Path(main_directory)
    if not main_dir.is_dir():
        print(f"Error: {main_directory} is not a valid directory.")
        return

    # Iterate over manga series folders
    for manga_folder in main_dir.iterdir():
        if not manga_folder.is_dir():
            continue

        series_name = manga_folder.name  # Get the series name

        # Iterate over chapter folders within each series
        for chapter_folder in manga_folder.iterdir():
            if not chapter_folder.is_dir():
                continue

            # Gather all image files in the chapter folder
            images = sorted(
                [file for file in chapter_folder.iterdir() if file.suffix.lower() in ['.jpg', '.jpeg', '.png']]
            )

            if not images:
                print(f"No images found in {chapter_folder}. Skipping...")
                continue

            # Define CBZ file path
            cbz_file_path = manga_folder / f"{chapter_folder.name}.cbz"
            print(f"Creating CBZ file: {cbz_file_path}")

            # Create the CBZ file
            with zipfile.ZipFile(cbz_file_path, 'w') as cbz_file:
                for image in images:
                    cbz_file.write(image, arcname=image.name)

            # Add metadata to the newly created CBZ file
            add_metadata_to_cbz(cbz_file_path, series_name)

            print(f"Finished creating {cbz_file_path}")

            # Delete the chapter folder
            print(f"Deleting folder: {chapter_folder}")
            shutil.rmtree(chapter_folder)

    # Update existing CBZ files without metadata
    update_existing_cbz_metadata(main_directory)

    print("All CBZ files created and updated successfully.")


def update_existing_cbz_metadata(main_directory):
    """
    Update existing CBZ files to include series metadata if not already present.
    """
    main_dir = Path(main_directory)
    for manga_folder in main_dir.iterdir():
        if not manga_folder.is_dir():
            continue

        series_name = manga_folder.name  # Get the series name

        for cbz_file in manga_folder.glob("*.cbz"):
            with zipfile.ZipFile(cbz_file, 'r') as zip_file:
                if "ComicInfo.xml" in zip_file.namelist():
                    print(f"Metadata already present in {cbz_file}. Skipping...")
                    continue

            # Add metadata if not present
            add_metadata_to_cbz(cbz_file, series_name)

main_directory = r"C:\Users\user\Documents\Mangas\MANGA"
create_cbz_from_folders(main_directory)
