import os
import re
import struct


#
# path - mri filepath
#
def parse(path: str):
    with open(path, "rb") as fs:
        idata = fs.read()

    dirpath = os.path.dirname(path)
    name = re.match(r"(\w+)\.\w+$", path).group(1)
    filepath_noext = os.path.join(dirpath, name)
    size_list = [0] * 4
    size = len(idata)
    header_size = size + 7

    # little endian byte representation
    # zeros to the right don't change the value
    for i, byte in enumerate(struct.pack("<I", header_size)):
        size_list[i] = byte

    odata = [
        82,  # R
        73,  # I
        70,  # F
        70,  # F
        size_list[0],
        size_list[1],
        size_list[2],
        size_list[3],
        87,  # W
        69,  # E
        66,  # B
        80,  # P
        86,  # V
        80,  # P
        56,  # 8
    ]

    for bit in idata:
        odata.append(101 ^ bit)

    opath = f"{filepath_noext}_p.webp"
    with open(opath, "wb") as fs:
        fs.write(bytes(odata))

    print(f"{opath} written")


def main(args):
    for path in args:
        parse(path)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
