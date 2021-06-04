# RopZ (rp++ organizer)

Takes output from [rp++](https://github.com/0vercl0k/rp) and organizes it to make finding helpful gadgets a bit quicker.

Created while studying for the OSED course.

## Usage

`.\rp-win-x86.exe -f ... -r 5 > rop.txt`\
`python3 ropZ.py rop.txt`

## Modifying

The gadget search stuff can be easily modified in the `SETTINGS` section, where the `cfg` dictionary is defined. 

To add / change searchs, you just need to follow the following format:

```
cfg = {
    "NAME": r"REGEX",
    "NAME2": r"REGEX2",
    ...
}
```