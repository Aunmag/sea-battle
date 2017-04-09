import cx_Freeze

import constants

cx_Freeze.setup(
    name=constants.TITLE,
    version=constants.VERSION,
    author=constants.AUTHOR,
    description=constants.DESCRIPTION,
    executables=[
        cx_Freeze.Executable("sea_battle.py"),
    ],
)
