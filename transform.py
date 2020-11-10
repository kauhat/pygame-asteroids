from __future__ import annotations

from typing import Optional, Union
import components as c


class TransformChain:
    def __init__(self, parent: Optional[TransformChain] = None) -> None:
        self.parent = parent

    def stack(self, stack: list[c.Transform]) -> c.Transform:
        stacked = c.Transform()

        for trans in stack:
            stacked.position += trans.position.rotate(stacked.angle)
            stacked.angle += trans.angle

        return stacked
