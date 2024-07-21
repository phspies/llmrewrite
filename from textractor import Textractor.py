from textractor import Textractor
from textractor.data.constants import TextractFeatures

def main():
    extractor = Textractor(region_name="us-west-2")

    document = extractor.start_document_analysis(
        file_source="your_file.pdf",
        features=[TextractFeatures.LAYOUT],
        s3_upload_path="s3://sample_bucket/sample_path",
        save_image=True
    )

    for i, page in enumerate(document.pages):
        for j, figure in enumerate(page.page_layout.figures):
            bbox = figure.bbox
            width, height = page.image.size

            figure_image = page.image.crop((
                bbox.x * width,
                bbox.y * height,
                (bbox.x + bbox.width) * width,
                (bbox.y + bbox.height) * height
            ))

            figure_image.save(f"page_{i+1}_figure_{j+1}.jpeg")

if __name__ == "__main__":
    main()