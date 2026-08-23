# Download Clearner

A small Python utility that keeps the Downloads folder clean automatically.

I built this because my Downloads folder was gradually filling up with old files and folders. When there are a lot of items in Downloads, finding recently downloaded files becomes more annoying and the folder can take a little longer to load and browse.

This script automatically moves items that have not been accessed for more than 3 days into a separate `OldDownloads` folder.

## How It Works

The script:

1. Checks the top-level items inside `Downloads`.
2. Looks at their last access time.
3. Finds items that have not been accessed for more than 3 days.
4. Moves them to `Downloads/OldDownloads`.


## Automatic Cleanup

The script is designed to run automatically using the operating system's task scheduler, it can be added to **Task Scheduler** and configured to run periodically in the background. This means the Downloads folder can stay clean without having to manually run the script.

## Why I Made It

I wanted a simple solution to keep my Downloads folder manageable.

Instead of deleting old files, the script moves them to `OldDownloads`, so they are still available if I need them later.

## Requirements

* Python 3
* Standard Python libraries only

No external packages are required.

## Usage

Run the script manually with:

```bash
python main.py
```

Or configure it with your system's task scheduler to run automatically.

