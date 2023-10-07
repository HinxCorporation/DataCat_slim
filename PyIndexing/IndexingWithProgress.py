import os
from tqdm import tqdm


def test_index_an_folder_with_slide(path):
    """
    此方法没啥用, 不用测试了.
    :param path:
    :return:
    """
    file_count = sum(len(files) for _, _, files in os.walk(path))  # Get the total number of files

    with tqdm(total=file_count, desc="Progress", unit="file") as pbar:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                # Process each file here
                # ...

                pbar.update(1)  # Update the progress bar
