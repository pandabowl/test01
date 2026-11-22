"""
Stale notes in package descriptions that contradict what the package includes.

Each entry is (old, new): merge_live.py replaces `old` with `new` in the live
description. `old` is copied exactly from the live HTML as Shopify stores it.
Once a fix is live, `old` is gone and the entry does nothing, so re-running
is safe.

Left alone on purpose:
- "The Optional Furniture Kit (not included)" on the Super Dragon, Dragon and
  Bull Elk Pro/Studio packages: those packages really don't include a kit.
- "Optional" accessories that really are optional (Type-S thermocouple,
  Cone 6 starter kit, kiln stands on the TnF-23-3/24-3, colors).
"""

LL_SAVE_MORE = (
    '<br>Save even more when you order the furniture kit of shelves and posts when you '
    'order with a new kiln. <br>The vent system is a highly recommended option. It is very '
    'important to have the down-draft vent when the kiln is installed in a basement or other '
    'living space. <br>',
    '<br>The furniture kit of shelves and posts and the Vent-Sure downdraft vent are both '
    'included in this package. The vent is very important when the kiln is installed in a '
    'basement or other living space. <br>',
)

LL_CHOOSE_OPTIONS_SUPER = (
    '<br><span style="font-size: 12pt;">Note: The prices shown above in "Choose your options" '
    'for Furniture kit and Vent are also super discounted ! Use the check boxes and the update '
    'price button above to tune your package to fit your budget. </span>',
    '',
)

PARAGON_OPTIONAL_KIT = [
    ("The Optional Furniture Kit", "The Furniture Kit (included in this package)"),
    ("When estimating the price of the kiln, include the cost of furniture. ", ""),
]

TEXT_FIXES = {
    # L&L e23M-3 Easy-Fire package
    "8315914289474": [
        LL_SAVE_MORE,
        ('<span style="font-family: Arial,Helvetica,Geneva,Swiss,SunSans-Regular,Trebuchet MS; '
         'color: #000000;"><span style="font-size: 12pt;">Note: Furniture kit and Vent are also '
         'discounted prices ! Use the check boxes and the update price button above to tune your '
         'package to fit your budget. </span></span><br>', ''),
        LL_CHOOSE_OPTIONS_SUPER,
    ],
    # L&L e23S-3 Easy-Fire package
    "8315914649922": [LL_SAVE_MORE, LL_CHOOSE_OPTIONS_SUPER],
    # L&L e28M-3 Easy-Fire package
    "8315915469122": [
        ('<br><span style="font-size: 12pt;">Note: The prices shown above in "Choose your options" '
         'for Furniture kit and Vent are also discounted! Use the check boxes and the update price '
         'button above to tune your package to fit your budget. <br><br></span>', '<br>'),
    ],
    # L&L e28S-3 Easy-Fire package
    "8315915796802": [
        ('<br><span style="font-size: 12pt;">Note: Use the check boxes and the update price button '
         'above to tune your package to fit your budget. <br><br></span>', '<br>'),
    ],
    # Paragon TnF-82 and TnF-82-3 packages (drafts): the kit is included
    "8304899817794": PARAGON_OPTIONAL_KIT,
    "8304899883330": PARAGON_OPTIONAL_KIT,
    # Bull Elk Pro package: the VentMaster is included
    "8316071543106": [
        ("Order the optional Orton Vent Master, which mounts to the back of the kiln.",
         "Included here is the Orton Vent Master, which mounts to the back of the kiln."),
    ],
}
