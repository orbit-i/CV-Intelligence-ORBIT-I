import os
import zipfile


def export_offers_as_zip():
    """
    Reads all .docx files from data/output/, bundles them into a single
    ZIP file, and saves it as data/output/offer_letters.zip.

    Returns:
        str: Path to the created ZIP file.
    """
    output_dir = os.path.join("data", "output")
    zip_path = os.path.join(output_dir, "offer_letters.zip")

    if not os.path.exists(output_dir):
        raise FileNotFoundError(f"Output folder not found: {output_dir}")

    # Get all .docx files in the output folder
    docx_files = [
        f for f in os.listdir(output_dir)
        if f.lower().endswith(".docx")
    ]

    if not docx_files:
        raise FileNotFoundError("No .docx files found in data/output/ to zip.")

    # Create the ZIP file
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_name in docx_files:
            file_path = os.path.join(output_dir, file_name)
            # arcname keeps only the filename inside the zip (no folder path)
            zipf.write(file_path, arcname=file_name)

    return zip_path


if __name__ == "__main__":
    path = export_offers_as_zip()
    print(f"ZIP created at: {path}")
    
