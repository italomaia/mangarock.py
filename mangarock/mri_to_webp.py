import re
import struct


def parse_mri_data_to_webp_buffer(data):
    size_list = [0] * 4
    size = len(data)
    header_size = size + 7

    # little endian byte representation
    # zeros to the right don't change the value
    for i, byte in enumerate(struct.pack("<I", header_size)):
        size_list[i] = byte

    buffer = [
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

    for bit in data:
        buffer.append(101 ^ bit)

    return buffer


def parse_mri_path_to_webp_buffer(path: str):
    with open(path, "rb") as fs:
        idata = fs.read()

    return parse_mri_data_to_webp_buffer(idata)


#
# path - mri filepath
#
def parse_to_file(path: str, opath: str = None):
    with open(path, "rb") as fs:
        data = fs.read()

    buffer = parse_mri_data_to_webp_buffer(data)

    filepath_noext = re.match(r"(.*)\.\w+$", path).group(1)
    opath = opath or f"{filepath_noext}.webp"

    with open(opath, "wb") as fs:
        fs.write(bytes(buffer))

    print(f"{opath} written")


def main(args):
    for path in args:
        parse_to_file(path)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
