import itertools
from typing import List, Sequence

from d4dj_utils.master.music_master import MusicMaster
from d4dj_utils.master.music_mix_master import MusicMixMaster


def get_best_mix(songs: Sequence[MusicMaster]):
    songs = sorted(songs, key=lambda s: s.id)
    best_rating = 0
    best_mix = []
    for mix in itertools.permutations(songs):
        rating = calculate_mix_rating(mix)
        if rating > best_rating:
            best_rating = rating
            best_mix = mix
    return best_mix


def calculate_mix_rating(songs: Sequence[MusicMaster]) -> int:
    try:
        from d4dj_utils.extended.chart.mix import calculate_mix_rating
    except ImportError as e:
        raise RuntimeError("Extended features not available") from e
    return calculate_mix_rating(songs)


def get_mix_data(songs: Sequence[MusicMaster]) -> List[MusicMixMaster]:
    if len(songs) < 2:
        raise ValueError("Song list must have length of at least 2.")
    for song in songs:
        if not (len(song.mix_info) == 3):
            raise ValueError(
                f"Song {song.name_description} does not have valid mix data."
            )
    return (
        [songs[0].mix_info[1]]
        + [song.mix_info[2] for song in songs[1:-1]]
        + [songs[-1].mix_info[3]]
    )
