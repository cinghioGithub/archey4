"""System load average detection module"""

import os
from contextlib import suppress

from archey.entry import Entry
from archey.colors import Colors


class LoadAverage(Entry):
    """System load average detection entry"""

    _PRETTY_NAME = "Load Average"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with suppress(AttributeError):
            self.value = os.getloadavg()

    def output(self, output) -> None:
        if not self.value:
            # Fall back on the default behavior if load average values could not be detected.
            super().output(output)
            return

        # DRY constant thresholds.
        warning_threshold = self.options.get("warning_threshold", 1.0)
        danger_threshold = self.options.get("danger_threshold", 2.0)

        output.append(
            self.name,
            " ".join(
                [
                    str(Colors.get_level_color(load_avg, warning_threshold, danger_threshold))
                    + str(load_avg)
                    + str(Colors.CLEAR)
                    for load_avg in self.value
                ]
            ),
        )