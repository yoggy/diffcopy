# diffcopy.py
```
 py diffcopy.py -h
usage: diffcopy.py [-h] [-d] [--exclude-filenames EXCLUDE_FILENAMES [EXCLUDE_FILENAMES ...]] [--exclude-exts EXCLUDE_EXTS [EXCLUDE_EXTS ...]] original_dir target_dir destination_dir

Copy only the files that have changed.

positional arguments:
  original_dir          Original Directory
  target_dir            Target Directory
  destination_dir       Destination directory

options:
  -h, --help            show this help message and exit
  -d, --dry-run         dry run mode
  --exclude-filenames EXCLUDE_FILENAMES [EXCLUDE_FILENAMES ...]
                        exclude filenames
  --exclude-exts EXCLUDE_EXTS [EXCLUDE_EXTS ...]
                        exclude extentions
```

## Copyright and license

Copyright (c) 2024 yoggy

Released under the [MIT license](LICENSE)
 