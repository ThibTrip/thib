"""
Helpers for interacting more easily with `faster_whisper` especially when it comes
to generating subtitles.

Notes
-----
The code is quite strict / opionated (e.g. additional parameters cannot be passed for the transcription
than the ones I manually defined) as it was not meant to be shared initially and I did
not take time to "generalize" it more.
"""
import json
import os
from dataclasses import dataclass, field as dataclass_field
from faster_whisper import WhisperModel
from faster_whisper.transcribe import Segment, Word
from loguru import logger
from pathlib import Path
from whisper.utils import get_writer
from typing import Any, Literal, TypeAlias, TYPE_CHECKING
from tqdm import tqdm


if TYPE_CHECKING:
    import pandas as pd


# types and type aliases
OpenAPISegmentData: TypeAlias = list[dict[str, Any]]


@dataclass(frozen=True)
class TranscriptionResult:
    """
    Stores the result of a transcription of given media file at path `media_filepath`
    """
    media_filepath: Path
    source_language: str
    segments_data: OpenAPISegmentData
    is_translation: bool
    srt_writer: Any = dataclass_field(init=False)

    def __post_init__(self) -> None:
        srt_writer = get_writer(output_format='srt', output_dir='.')
        object.__setattr__(self, 'srt_writer', srt_writer)

    def to_srt(self, path: str | None = None) -> None:
        """
        Stores the transcription data as a subtitle file.
        If a `path` is not provided, it is automatically generated by using
        the path of the media and renaming its extension to `.srt`.
        """
        media_filepath = self.media_filepath  # alias

        # generate subtitles to the default path
        self.srt_writer(result={'segments': self.segments_data}, audio_path=media_filepath)

        # move output file to our desired path (there are other ways to do that but they are annoying
        # e.g. using your own writer)
        default_filepath = Path.cwd() / media_filepath.with_suffix('.srt').name
        language_suffix = 'en' if self.is_translation else self.source_language
        if path is None:
            desired_stem = f'{media_filepath.stem}_{language_suffix}'
            desired_filepath = media_filepath.with_stem(desired_stem).with_suffix('.srt')
        else:
            desired_filepath = path

        logger.info(f'Saving subtitles: {str(default_filepath)} -> {str(desired_filepath)}')
        if os.path.exists(desired_filepath):
            logger.warning(f'Overwriting already existing file {desired_filepath}')
            os.remove(desired_filepath)
        os.rename(default_filepath, desired_filepath)

    def to_json(self, path: str | None = None) -> None:
        """
        Saves the data of the transcription (only the segments) to a JSON file.
        If a `path` is not provided, it is automatically generated by using
        the path of the media and renaming its extension to `.json`.
        """
        if path is None:
            json_segments_path = Path(self.media_filepath).with_suffix('.json')
        else:
            json_segments_path = path
        with open(json_segments_path, mode='w', encoding='utf-8') as fp:
            json.dump(obj=self.segments_data, fp=fp, ensure_ascii=False, indent=4)

    def to_string(self) -> str:
        """
        Concatenates the texts from all segments as a single string joined by line
        breaks.
        """
        return '\n'.join([d['text'] for d in self.segments_data])

    @property
    def segments_dataframe(self) -> 'pd.DataFrame':
        try:
            import pandas as pd
        except (ModuleNotFoundError, ImportError) as e:
            raise ModuleNotFoundError('Optional dependency `pandas` needs to be installed') from e
        return pd.DataFrame(self.segments_data).set_index('id')


def faster_whisper_segment_to_openapi_whisper_segment(segment: Segment) -> dict[str, Any]:
    """
    Converts faster whisper segments to OpenAI segments.
    This is useful for using whisper utilities such as writing subtitles.

    Examples
    --------
    >>> from pprint import pprint
    >>> segment_example = Segment(id=3, seek=9000, start=60.0, end=89.9, text=' Дякую за перегляд!',
    ...                           tokens=[50365, 3401, 681, 35119, 4396, 4321, 4953, 2873, 856, 0, 51864],
    ...                           temperature=0.0, avg_logprob=-0.08813476438323657,
    ...                           compression_ratio=0.7857142857142857, no_speech_prob=0.043487548828125,
    ...                           words=[Word(start=60.0, end=66.94, word=' Дякую', probability=0.09035746256510417),
    ...                                  Word(start=66.94, end=67.36, word=' за', probability=0.01708984375),
    ...                                  Word(start=67.36, end=89.9, word=' перегляд!', probability=0.83758544921875)])
    >>> pprint(faster_whisper_segment_to_openapi_whisper_segment(segment), sort_dicts=False)
    {'id': 3,
     'seek': 9000,
     'start': 60.0,
     'end': 89.9,
     'text': ' Дякую за перегляд!',
     'tokens': [50365, 3401, 681, 35119, 4396, 4321, 4953, 2873, 856, 0, 51864],
     'temperature': 0.0,
     'avg_logprob': -0.08813476438323657,
     'compression_ratio': 0.7857142857142857,
     'no_speech_prob': 0.043487548828125,
     'words': [{'start': 60.0,
                'end': 66.94,
                'word': ' Дякую',
                'probability': 0.09035746256510417},
               {'start': 66.94,
                'end': 67.36,
                'word': ' за',
                'probability': 0.01708984375},
               {'start': 67.36,
                'end': 89.9,
                'word': ' перегляд!',
                'probability': 0.83758544921875}]}
    """
    # Note: `_asdict` is not a private method per say, it is a documented method of named tuples
    # and `FasterWhisperSegment` is one. Same goes for `FasterWhisperWord`.
    segment_dict = segment._asdict()
    words: list[Word] | None = segment_dict['words']
    if words is not None:
        words_parsed = [word._asdict() for word in words]
    else:
        words_parsed = None
    segment_dict['words'] = words_parsed
    return segment_dict


@dataclass(frozen=True)
class WhisperTranscriber:
    """
    Transcribes given media using whisper.

    Parameters
    ----------
    model :
        An OpenAI Whisper model e.g. "large-v3"

    media_filepath :
        Path of given media

    source_language :
        ISO 639-1 language code e.g. "it" for Italian

    initial_prompt :
        This provides more context for the transcription.
        IMPORTANT: it should match the language of the audio for optimal transcription accuracy

    condition_on_previous_text :
        When `condition_on_previous_text` is set to `True`, Whisper takes into account the text it has already
        transcribed in the current session to inform its ongoing transcription decisions.
        This can help in maintaining the coherence and context of the conversation or speech being transcribed.
        But it may also cause hallucinations loops where the model keeps repeating itself regardless of whatever
        is actually being said.
        Setting `condition_on_previous_text` to `False` will treat each segment independently.

    task :
        Use the default value 'transcribe' to generate segments and subtitles in the source language of the media.
        Use value 'translate' to generate segments and subtitles translated into English.

        IMPORTANT: subtitles generated when transcribing and translating have different timings, making them very
        impractical for watching a media with the two subtitles display at once.
    """
    model: WhisperModel
    media_filepath: Path
    source_language: str
    initial_prompt: str | None = None
    condition_on_previous_text: bool = True
    task: Literal['translate', 'transcribe'] = 'transcribe'

    def __post_init__(self):
        if isinstance(self.media_filepath, str):
            media_filepath = Path(self.media_filepath)
        else:
            media_filepath = self.media_filepath
        object.__setattr__(self, 'media_filepath', media_filepath.resolve())

    def transcribe(self) -> TranscriptionResult:
        # prepare generator of segments + get some info on the media
        segments_gen, info = self.model.transcribe(audio=str(self.media_filepath),  # Path objects not supported
                                                   word_timestamps=True,
                                                   language=self.source_language,
                                                   task=self.task,
                                                   initial_prompt=self.initial_prompt,
                                                   condition_on_previous_text=self.condition_on_previous_text)
        media_duration = round(info.duration, 2)
        logger.info(f'File "{self.media_filepath}" has a length of {media_duration} audio seconds')

        # prepare generator iteration
        current_time = 0
        segments_data = []

        # get transcription from segments
        with tqdm(total=media_duration, unit=' audio seconds') as progress_bar:
            for ix, segment in enumerate(segments_gen):
                # convert named tuples to dict
                segment_data = faster_whisper_segment_to_openapi_whisper_segment(segment=segment)
                segments_data.append(segment_data)

                # show progress
                progress_bar.update(segment.end - current_time)

                # set the new current time for the next loop
                current_time = segment.end

        return TranscriptionResult(media_filepath=self.media_filepath, source_language=self.source_language,
                                   segments_data=segments_data, is_translation=self.task == 'translate')