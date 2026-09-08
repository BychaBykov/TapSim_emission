#!/usr/bin/env python3
import sys

GEN_FILE   = "output.txt"
MESH_IN    = "CPDEmitter.txt"
MESH_OUT   = "CPDEmitterFix.txt"
ANODE_ID   = 1
EMITTER_ID = 10
ANODE_POT  = 1000.0
RND        = 13


def read_header(line):
    parts = line.split()
    if not parts or parts[0].upper() != "ASCII":
        raise SystemExit("mesh file is not ASCII, set ASCII_OUTPUT_MODE = 1 in meshgen.ini")
    count = int(parts[1])
    with_numbers = int(parts[2]) if len(parts) > 2 else 0
    with_potentials = int(parts[3]) if len(parts) > 3 else 0
    return count, with_numbers, with_potentials


def load_generator(path):
    gen = {}
    with open(path) as f:
        _, wn, wp = read_header(f.readline())
        if not wp:
            raise SystemExit("generator file has no potential column")
        pot_col = 5 if wn else 4
        for line in f:
            s = line.split()
            if len(s) <= pot_col:
                continue
            key = (round(float(s[0]), RND), round(float(s[1]), RND), round(float(s[2]), RND))
            gen[key] = float(s[pot_col])
    return gen


def main():
    gen = load_generator(GEN_FILE)
    print("generator nodes: %d" % len(gen))

    fin = open(MESH_IN)
    count, wn, wp = read_header(fin.readline())
    print("mesh header: count=%d withNumbers=%d withPotentials=%d" % (count, wn, wp))

    if not wp:
        raise SystemExit("mesh has no potential column; cannot set potentials")

    pot_col = 5 if wn else 4

    fout = open(MESH_OUT, "w")
    fout.write("ASCII %d %d %d\n" % (count, wn, wp))

    n_anode = n_emitter = n_matched = n_lines = 0

    for line in fin:
        s = line.split()
        if len(s) <= pot_col:
            continue

        x, y, z = float(s[0]), float(s[1]), float(s[2])
        tid = int(s[3])
        number = s[4] if wn else None
        pot = float(s[pot_col])

        if tid == ANODE_ID:
            pot = ANODE_POT
            n_anode += 1
        elif tid == EMITTER_ID:
            n_emitter += 1
            key = (round(x, RND), round(y, RND), round(z, RND))
            if key in gen:
                pot = gen[key]
                n_matched += 1

        fields = ["%.10e" % x, "%.10e" % y, "%.10e" % z, str(tid)]
        if wn:
            fields.append(number)
        fields.append("%.10e" % pot)

        fout.write("\t".join(fields) + "\n")
        n_lines += 1

    fin.close()
    fout.close()

    print("written lines: %d (header count %d)" % (n_lines, count))
    print("anode nodes set: %d" % n_anode)
    print("emitter nodes: %d, matched with generator: %d" % (n_emitter, n_matched))

    if n_lines != count:
        print("WARNING: line count does not match header")
    if n_emitter and n_matched != n_emitter:
        print("WARNING: %d emitter nodes had no generator match" % (n_emitter - n_matched))


if __name__ == "__main__":
    main()