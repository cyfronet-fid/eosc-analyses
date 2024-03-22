from tqdm import tqdm

from settings import settings
from dump_analyzer.data_loader.data_loader import process_and_save_data
from dump_analyzer.data_loader.schema.model_2024_01.reserch_product import ResearchProduct
from dump_analyzer.process_metadata.process_metadata import process_metadata

if __name__ == "__main__":
    with tqdm(total=len(settings.COLLECTIONS), desc="Initializing...") as pbar:
        for collection in settings.COLLECTIONS:
            pbar.set_description(f"Processing {collection}")
            process_and_save_data(
                settings.COLLECTIONS[collection]["INPUT_PATH"], ResearchProduct
            )
            pbar.update(1)

        pbar.update(1)

    process_metadata(settings.METADATA_PATH)