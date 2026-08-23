import os
import shutil
import time


class DownloadCleaner:
    """
    Keeps the Downloads folder manageable by moving
    inactive files and folders into OldDownloads.

    Files are checked using their last access time.

    For folders, only one file inside the folder is checked.
    If that file is older than the configured threshold,
    the entire folder is moved without scanning every item.
    """

    def __init__(self):
        # The folder we want to keep clean
        self.source_folder = os.path.expanduser("~/Downloads")

        # Storage for items that have not been accessed recently
        self.destination_folder = os.path.join(
            self.source_folder,
            "OldDownloads"
        )

        # Items older than 3 days are considered old
        self.three_days = 3 * 24 * 60 * 60

        # Capture the current time once for this cleanup run
        self.now = time.time()

        # Create the destination if it does not exist
        os.makedirs(self.destination_folder, exist_ok=True)

    def find_first_file(self, folder_path):
        """
        Find the first file inside a folder.

        This walks through nested folders, but stops immediately
        after finding one file. We don't need to inspect everything
        because the first file is used as the folder's age reference.
        """

        for root, directories, files in os.walk(folder_path):

            # We only need one file
            if files:
                return os.path.join(root, files[0])

        # Folder contains no files
        return None

    def is_old(self, file_path):
        """Check whether a file has not been accessed for 3+ days."""

        try:
            access_time = os.path.getatime(file_path)
        except FileNotFoundError:
            return False

        return self.now - access_time > self.three_days

    def move_item(self, item_path):
        """Move an old item into OldDownloads."""

        item_name = os.path.basename(item_path)
        destination_path = os.path.join(
            self.destination_folder,
            item_name
        )

        try:
            shutil.move(item_path, destination_path)

            print(f"Moved: {item_name}")
            print("   -> OldDownloads/")

        except Exception as error:
            print(f"Failed: {item_name}")
            print(f"   -> {error}")

    def process_item(self, item_name):
        """Check one item from the Downloads folder."""

        # OldDownloads must never be processed.
        if item_name == "OldDownloads":
            return

        item_path = os.path.join(
            self.source_folder,
            item_name
        )

        try:
            if os.path.isfile(item_path):
                # Regular file: check the file itself
                if self.is_old(item_path):
                    self.move_item(item_path)

            elif os.path.isdir(item_path):
                # Folder: find one file somewhere inside it
                first_file = self.find_first_file(item_path)

                # Empty folders are left alone
                if first_file is None:
                    return

                # If the sample file is old, move the whole folder
                if self.is_old(first_file):
                    self.move_item(item_path)

        except FileNotFoundError:
            # The item may have been moved/deleted while the script ran
            pass

        except Exception as error:
            print(f"Failed to process: {item_name}")
            print(f"   -> {error}")

    def clean(self):
        """Run the Downloads cleanup."""

        print("\n" + "=" * 55)
        print("              DOWNLOADS CLEANER")
        print("=" * 55)
        print(f"Checking: {self.source_folder}")
        print(f"Archive:  {self.destination_folder}")
        print("Looking for items not accessed in 3+ days...")
        print("-" * 55)

        try:
            # Only list the immediate contents of Downloads.
            # IMPORTANT:
            # OldDownloads is not opened or scanned here.
            # Even if it contains 100,000 files, they are untouched.
            items = os.listdir(self.source_folder)

        except FileNotFoundError:
            print("Downloads folder was not found.")
            return

        for item_name in items:
            self.process_item(item_name)

        print("-" * 55)
        print("Cleanup completed successfully.")
        print("=" * 55 + "\n")


if __name__ == "__main__":
    cleaner = DownloadCleaner()
    cleaner.clean()
