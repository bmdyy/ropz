#!/usr/bin/python3

# William Moody
# 04.06.2021

# ===== INIT

import sys
import re

if len(sys.argv) != 3:
    print("Usage: %s rop.txt <output file>" % sys.argv[0])
    print("  -- rop.txt = output from ./rp++ -f ... -r 5 > rop.txt")
    print("  -- <output file> is where the parsed contains will end up")
    sys.exit(1)

print()
print("> RopZ (rp++ organizer) <")
print("> William Moody         <")
print("> 04.06.2021            <")
print()

# ===== SETTINGS

fname = sys.argv[1] # File which contains rp++ output
outname = sys.argv[2] # File which will contain the new output
seperator = " | " # Used when outputting gadgets
max_retn = 0x10 # Highest value for a retn
ignore_ebp = True # Don't allow gadgets which mess up ebp

cfg = {
    "(Clean) Deref": r"^mov e.., dword \[e..\] ; ret",
    "(Clean) Swap": r"^xchg e.., e.. ; ret",
    "(Clean) Move": r"^mov e.., e.. ; ret",
    "(Clean) Add": r"^add e.., e.. ; ret",
    "(Clean) Sub": r"^sub e.., e.. ; ret",
    "(Clean) Pop": r"^pop e.. ; ret",
    "(Clean) Neg": r"^neg e.. ; ret",
    "(Clean) Inc": r"^inc e.. ; ret",
    "(Clean) Dec": r"^dec e.. ; ret",
    # "(Clean) Ret": r"^ret  ;",
    "(Clean) Write": r"^mov dword \[e..\], e.. ; ret",
    "Get ESP": r"push esp.*pop e.*ret"
}

# ===== LOAD RP++ OUTPUT

# Will hold all gadgets and their addresses
# as a 2d array
all = []

# rp++ outputs a file in utf-16-le mode for some
# reason, so specifying the encoding mode is
# necessary here
with open(fname, 'r', encoding='utf-16-le') as f:
    for line in f:
        # Check for a ';', so that we can skip
        # over the first text lines
        if ';' in line:
            line = line.strip()
            addr = line[0:10]
            asm = " ".join(line.split(" ")[1:-3])
            all.append((addr, asm))

print("[+] Loaded %d gadgets..." % len(all))

# ===== SEARCH THE GADGETS

# Inits the config by adding an empty array
# so that we don't need to do it manually (looks better)
for k, v in cfg.items():
    cfg[k] = [v, []]

# Loop through all gadgets
for gadget in all:
    # Loop through all configured searchs
    for k, v in cfg.items():
        # Check if the current gadget regexp matches this gadget
        if re.search(v[0], gadget[1]):
            # Ignore the gadgets which have a retn 0x... over our max_retn
            if "retn 0x" in gadget[1]:
                if int(gadget[1].split(" ")[-2:][0], 16) > max_retn:
                    continue

            # Ignore the gadgets which mess with ebp
            if ignore_ebp and "ebp" in gadget[1]:
                continue

            # Add good gadgets to the list
            cfg[k][1].append(gadget)

# ===== DISPLAY RESULTS

# Open the output file
f = open(outname, "w")

# Loop through the config
for k, v in cfg.items():
    # Print the current search regexp and all gadgets which
    # were found to match
    title  = "%s gadgets [%d]" % (k, len(v[1]))
    print("[+] Found %d \"%s\" gadgets..." % (len(v[1]), k))
    f.write(title + "\n" + "=" * len(title) + "\n")
    for i in range(len(v[1])):
        f.write(seperator.join(v[1][i]) + "\n")
    f.write("\n")

# Save the file
f.flush()
f.close()

print("[+] Output saved to %s" % outname)
print()