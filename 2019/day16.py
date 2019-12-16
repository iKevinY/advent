import fileinput


PATTERN = [0, 1, 0, -1]
SIGNAL = [int(s) for s in fileinput.input()[0].strip()]


def fft(signal):
    def coeff(idx, digit):
        r = ((idx + 1) // (digit + 1)) % 4
        return PATTERN[r]

    for _ in range(100):
        for i in range(len(signal)):
            res = 0
            for j, d in enumerate(signal):
                res += coeff(j, i) * d

            signal[i] = abs(res) % 10

    return signal


def fft_backhalf(signal):
    # What pattern?
    for _ in range(100):
        partial = 0
        for i in reversed(range(len(signal) // 2, len(signal))):
            partial += signal[i]
            signal[i] = partial % 10

    return signal


part_1 = ''.join(str(n) for n in fft(SIGNAL[:]))[:8]
print "First 8 digits of FFT(input):", part_1

offset = int(''.join(str(n) for n in SIGNAL[:7]))
part_2 = ''.join(str(n) for n in fft_backhalf(SIGNAL * 10000)[offset:offset+8])
print "Offset digits of FFT(input * 10000):", part_2
