"""settings_example.py
    Rename this file to settings.py and python will its settings.
    settings.py is not, but settings_example.py is version tracked."""

# 1 MB, largest file to upload
MAX_CONTENT_LENGTH = 1 * 1024 * 1024

# 2 MB, size of directory
FOLDER_SIZE_LIMIT = 2 * 1024 * 1024

# maximum number of files
FILE_COUNT_LIMIT = 5

# the files that should not be listed
IGNORE_FILES = {"README.md"}

# file logs: uploads and deletes
LOG_FNAME = "flask_events.log"
