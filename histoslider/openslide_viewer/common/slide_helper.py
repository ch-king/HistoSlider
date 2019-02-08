from typing import List, Tuple

import openslide
from PyQt5.QtCore import QRectF


class SlideHelper:
    def __init__(self, slide_path: str):
        self._slide_path = slide_path
        with openslide.open_slide(slide_path) as slide:
            self.level_downsamples = slide.level_downsamples
            self.level_dimensions = slide.level_dimensions
            self.level_count = slide.level_count

    @property
    def slide_path(self) -> str:
        return self._slide_path

    @property
    def max_level(self) -> int:
        return len(self.level_downsamples) - 1

    @property
    def levels(self) -> List[int]:
        return list(range(self.level_count))

    def get_downsample_for_level(self, level: int) -> float:
        return self.level_downsamples[level]

    def get_level_size(self, level: int) -> Tuple[int, int]:
        return self.level_dimensions[level]

    def get_rect_for_level(self, level: int) -> QRectF:
        size = self.get_level_size(level)
        rect = QRectF(0, 0, size[0], size[1])
        return rect

    def get_best_level_for_downsample(self, downsample: float) -> int:
        with openslide.open_slide(self._slide_path) as slide:
            return slide.get_best_level_for_downsample(downsample)
