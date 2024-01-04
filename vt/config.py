"""
Contains vt configuration variables
    - `__build_dir__` - the directiory where the vanilla build will be dumped
    - `__public_dir__` - the directory where static files are stored. Default
                     is `"public"`
    - `__use_pub_dir__` - informs the vt compiler whether should move the
                         `__public_dir__` directory to the build directory
                          or dump its contents.
    - `__root__` - the root directory
    - `__index_files__` - the main html pages (at the `__root__` directory)
"""
import sys
import os


__build_dir__ = "__vt_build__"
__public_dir__ = "public"
__use_pub_dir__ = False
__root__ = "."
__index_files__ = []

# the index files are the .html files at the root dir
# if no args passed or first arg == "*":
#       build all
# else:
#       build the passed .html file

if not len(sys.argv[1:]) or sys.argv[1] == "*":
    __index_files__ = [f for f in os.listdir(__root__)]
else:
    __index_files__ = [file for file in sys.argv[1:]]

__index_files__ = [f for f in __index_files__ if f.endswith(".html")]
