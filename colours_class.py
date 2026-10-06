from collections import Counter
from PIL import Image


class Colours:
    def __init__(self, path):
        self.path = path
        self.image = Image.open(path)

        self.colours = []
        self.accents = []

    def extract_colours(self):
        quantized = self.image.quantize(
            colors=10,
            method=Image.Quantize.MEDIANCUT
        )

        palette = quantized.getpalette()

        self.colours = [
            tuple(palette[i:i + 3])
            for i in range(0, 30, 3)
        ]

        counts = Counter(quantized.getdata())

        self.select_accents(counts)

    def select_accents(self, counts):
        scored_colours = []

        for index, count in counts.items():
            r, g, b = self.colours[index]

            brightness = (r + g + b) / 3
            saturation = max(r, g, b) - min(r, g, b)

            if brightness <= 30 or brightness >= 245:
                continue

            brightness_score = 1 - abs(brightness - 128) / 128

            score = count * saturation * brightness_score

            scored_colours.append(
                (score, self.colours[index])
            )

        scored_colours.sort(reverse=True)

        self.accents = [
            colour
            for score, colour in scored_colours[:2]
        ]

    def get_accents(self):
        return self.accents