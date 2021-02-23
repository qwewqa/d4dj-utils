import dataclasses
import math
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

import msgpack
from PIL import Image, ImageDraw


class SoflanDiskTarget(Enum):
    Left = 1
    Right = 2
    Both = 3


class NoteType(Enum):
    Tap1 = 0  # dark
    Tap2 = 1  # light
    ScratchLeft = 2
    ScratchRight = 3
    StopStart = 4
    StopEnd = 5
    LongStart = 6
    LongMiddle = 7
    LongEnd = 8
    Slide = 9


@dataclass
class NoteData:
    lane: int
    type: NoteType
    time: float
    next_id: Optional[int] = None
    direction: Optional[int] = None
    effect_type: Optional[int] = None
    effect_parameter: Optional[float] = None

    @classmethod
    def from_serialized(cls, args):
        args = args[:]
        args[1] = NoteType(args[1])
        return cls(*args)

    def as_resolved(self):
        return ResolvedNote(self)


class ResolvedNote:
    def __init__(self, note_data):
        self.lane: int = note_data.lane
        self.type: NoteType = note_data.type
        self.time: float = note_data.time
        self.original_next_id: Optional[int] = note_data.next_id
        self.direction: Optional[int] = note_data.direction
        self.effect_type: Optional[int] = note_data.effect_type
        self.effect_parameter: Optional[float] = note_data.effect_parameter
        self.next: 'Optional[ResolvedNote]' = None
        self.prev: 'Optional[ResolvedNote]' = None

    def finalize(self, notes):
        if self.original_next_id:
            self.next = notes[self.original_next_id]
            self.next.prev = self

    def is_in(self, start_time, end_time, source=None):
        return (start_time <= self.time <= end_time and
                (self.type == NoteType.Slide or self.next is None or
                 self.next is source or self.next.is_in(start_time, end_time, self)) and
                (self.type == NoteType.Slide or self.prev is None or
                 self.prev is source or self.prev.is_in(start_time, end_time, self)))

    def to_data(self, notes):
        try:
            index = notes.index(self.next) if self.next else None
        except ValueError:
            index = None
        return NoteData(self.lane, self.type, self.time, index, self.direction, self.effect_type, self.effect_parameter)


@dataclass
class SoflanData:
    time: float
    velocity: float
    disks: SoflanDiskTarget

    @classmethod
    def from_serialized(cls, args):
        args = args[:]
        args[2] = SoflanDiskTarget(args[2])
        return cls(*args)


@dataclass
class Chart:
    song: str
    soflans: Tuple[SoflanData]
    bar_lines: Tuple[float]
    notes: Tuple[NoteData]

    @classmethod
    def from_msgpack(cls, data: bytes):
        data = msgpack.unpackb(data)
        data[1] = [SoflanData.from_serialized(sof) for sof in data[1]]
        data[3] = [NoteData.from_serialized(note) for note in data[3]]
        return cls(*data[0:4])

    def trim(self, start_time: float, end_time: float):
        soflans = tuple(dataclasses.replace(soflan, time=soflan.time - start_time)
                        for soflan in self.soflans if start_time <= soflan.time <= end_time)
        bar_lines = tuple(bar - start_time for bar in self.bar_lines if start_time <= bar <= end_time)
        notes = tuple(note.as_resolved() for note in self.notes)
        for note in notes:
            note.finalize(notes)
        notes = tuple(note for note in notes if note.is_in(start_time, end_time))
        notes = tuple(note.to_data(notes) for note in notes)
        notes = tuple(dataclasses.replace(note, time=note.time - start_time) for note in notes)
        return Chart(self.song, soflans, bar_lines, notes)

    def get_note_counts(self):
        counts = {
            'tap': 0,
            'scratch': 0,
            'stop': 0,
            'long': 0,
            'slide': 0,
            'tap1': 0,
            'tap2': 0,
            'scratch_left': 0,
            'scratch_right': 0,
            'stop_start': 0,
            'stop_end': 0,
            'long_start': 0,
            'long_middle': 0,
            'long_end': 0,
            'slide_tick': 0,
            'slide_flick': 0
        }

        for note in self.notes:
            if note.type == NoteType.Tap1:
                counts['tap'] += 1
                counts['tap1'] += 1
            elif note.type == NoteType.Tap2:
                counts['tap'] += 1
                counts['tap2'] += 1
            elif note.type == NoteType.ScratchLeft:
                counts['scratch'] += 1
                counts['scratch_left'] += 1
            elif note.type == NoteType.StopStart:
                counts['stop'] += 1
                counts['stop_start'] += 1
            elif note.type == NoteType.StopEnd:
                counts['stop'] += 1
                counts['stop_end'] += 1
            elif note.type == NoteType.ScratchRight:
                counts['scratch'] += 1
                counts['scratch_right'] += 1
            elif note.type == NoteType.LongStart:
                counts['long'] += 1
                counts['long_start'] += 1
            elif note.type == NoteType.LongMiddle:
                counts['long'] += 1
                counts['long_middle'] += 1
            elif note.type == NoteType.LongEnd:
                counts['long'] += 1
                counts['long_end'] += 1
            elif note.type == NoteType.Slide:
                counts['slide'] += 1
                if note.direction:
                    counts['slide_flick'] += 1
                else:
                    counts['slide_tick'] += 1

        return counts

    def render(self) -> Image:
        if not self.notes:
            return Image.new('RGB', (1, 1))

        super_scale = 2
        scale = 1

        width = 200
        height_per_second = 150
        padding = 15
        lane_width = 25
        lane_separator_width = 2
        barline_width = 1

        vertical_seconds = 10

        max_height = height_per_second * vertical_seconds
        width = int(width * scale * super_scale)
        height_per_second = int(height_per_second * scale * super_scale)
        padding = int(padding * scale * super_scale)
        lane_width = int(lane_width * scale * super_scale)
        lane_separator_width = int(lane_separator_width * scale * super_scale)
        barline_width = int(barline_width * scale * super_scale)
        max_height = int(max_height * scale * super_scale)

        height = math.ceil(max(note.time for note in self.notes) * height_per_second + 2 * padding)
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)

        draw.rectangle((-3.5 * lane_width + width / 2, 0, 3.5 * lane_width + width / 2, height), fill=(30, 30, 30))
        draw.rectangle((-3.5 * lane_width + width / 2, 0, -2.5 * lane_width + width / 2, height), fill=(60, 60, 60))
        draw.rectangle((2.5 * lane_width + width / 2, 0, 3.5 * lane_width + width / 2, height), fill=(60, 60, 60))

        for i in range(8):
            line_x = (i - 3.5) * lane_width + width / 2
            draw.line((line_x, 0, line_x, height), fill=(127, 127, 127), width=lane_separator_width)

        draw.line((0, padding, width, padding), fill=(150, 150, 150), width=barline_width)
        draw.line((0, height - padding, width, height - padding), fill=(90, 90, 90), width=barline_width)

        def center_coordinate_at(time: float, lane: int):
            return lane_width * (lane - 3) + width / 2, height - (time * height_per_second + padding)

        def note_center(note: NoteData):
            return center_coordinate_at(note.time, note.lane)

        for bar_time in self.bar_lines:
            bar_y = height - (bar_time * height_per_second + padding)
            draw.line((0, bar_y, width, bar_y), fill=(180, 180, 180), width=barline_width)

        note_colors = {
            NoteType.Tap1: (15, 20, 220),
            NoteType.Tap2: (90, 120, 255),
            NoteType.ScratchLeft: (255, 165, 0),
            NoteType.ScratchRight: (255, 165, 0),
            NoteType.StopStart: (255, 0, 0),
            NoteType.StopEnd: (255, 0, 0),
            NoteType.LongStart: (255, 223, 0),
            NoteType.LongMiddle: (255, 233, 0),
            NoteType.LongEnd: (255, 233, 0),
            NoteType.Slide: (255, 0, 255)
        }

        tap_types = {NoteType.Tap1, NoteType.Tap2}
        scratch_types = {NoteType.ScratchLeft, NoteType.ScratchRight}
        hold_types = {NoteType.StopStart, NoteType.StopEnd, NoteType.LongStart, NoteType.LongMiddle, NoteType.LongEnd}
        stop_types = {NoteType.StopStart, NoteType.StopEnd}
        long_types = {NoteType.LongStart, NoteType.LongMiddle, NoteType.LongEnd}

        for note in self.notes:
            if note.next_id is not None and note.next_id > 0:
                next_note = self.notes[note.next_id]

                if note.type in hold_types:
                    hold_width = 0.75 * lane_width
                else:
                    hold_width = 0.2 * lane_width

                color = tuple(math.floor(c * 0.8) for c in note_colors[note.type])

                if note.type in hold_types:
                    half_width = math.ceil(hold_width) / 2
                    x1, y1 = note_center(note)
                    x2, y2 = note_center(next_note)
                    draw.polygon((
                        x1 - half_width, y1,
                        x2 - half_width, y2,
                        x2 + half_width, y2,
                        x1 + half_width, y1
                    ), fill=color)
                else:
                    draw.line((note_center(note), note_center(next_note)), fill=color, width=math.ceil(hold_width))

            if note.type == NoteType.Slide:
                if note.direction != 0:
                    color = tuple(math.floor(c * 0.8) for c in note_colors[note.type])
                    cx, cy = note_center(note)
                    xy = (cx, cy - lane_width * 0.3,
                          center_coordinate_at(note.time, note.lane + note.direction)[0], cy,
                          cx, cy + lane_width * 0.3)
                    draw.polygon(xy, fill=color)

        for note in self.notes:
            cx, cy = note_center(note)
            color = note_colors[note.type]
            if note.type in tap_types or note.type in long_types:
                xy = (cx - lane_width * 0.6, cy - lane_width * 0.1, cx + lane_width * 0.6, cy + lane_width * 0.1)
                draw.rectangle(xy, fill=color)
            elif note.type in scratch_types or note.type in stop_types:
                xy = (cx - lane_width * 0.6, cy - lane_width * 0.6, cx + lane_width * 0.6, cy + lane_width * 0.6)
                draw.ellipse(xy, fill=color)
            elif note.type == NoteType.Slide:
                xy = (cx - lane_width * 0.2, cy - lane_width * 0.5, cx + lane_width * 0.2, cy + lane_width * 0.5)
                draw.ellipse(xy, fill=color)

        reformat_height = max_height if height >= max_height else height
        reformat_width = width * math.ceil(height / reformat_height)
        reformatted = Image.new('RGB', (reformat_width, reformat_height))
        for i in range(math.ceil(height / reformat_height)):
            region = img.crop((0, height - reformat_height * (i + 1), width, max(0, height - reformat_height * i)))
            reformatted.paste(region, (width * i, 0, width * (i + 1), reformat_height))
        reformatted = reformatted.resize((int(reformat_width / super_scale), int(reformat_height / super_scale)),
                                         Image.BOX)
        return reformatted


def load_chart(f):
    return Chart.from_msgpack(f.read())
