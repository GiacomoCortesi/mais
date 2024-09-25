from moviepy.editor import AudioFileClip
from spleeter.separator import Separator
import whisperx
import torch
import os
import uuid
import time
from pathlib import Path

class SubtitleService:
    def __init__(self, model_size="tiny", language=None, subtitles_frequency=5, speaker_detection=False, hugging_face_token="", separate_vocals=True, cache_path: Path = Path("/tmp/mais"), captions_path: Path = Path("captions")):
        self.model_size = model_size
        self.language = language
        self.subtitles_frequency = subtitles_frequency
        self.speaker_detection = speaker_detection
        self.hugging_face_token = hugging_face_token
        self.separate_vocals = separate_vocals

        self.id = uuid.uuid4()

        self.cache_path = cache_path / str(self.id)
        os.makedirs(self.cache_path)

        self.captions_path = captions_path
        os.makedirs(self.captions_path, exist_ok=True)
        # use CUDA if graphic cards allow it, fallback to CPU otherwise
        self.device: str = ""
        if torch.cuda.is_available():
           self.device = "cuda"
        else:
           self.device = "cpu"

    def _extract_audio_from_video(self, video_path: Path):
        # Create an AudioFileClip object
        audio = AudioFileClip(video_path)
        
        audio_file_path = self.cache_path / video_path.stem + '.mp3'
        
        # Write the audio to an .mp3 file
        audio.write_audiofile(audio_file_path)
        
        return audio_file_path
    
    def _extract_vocals_from_audio(self, audio_path):
        # Using 'spleeter:2stems' pre-trained model for voice and accompaniment separation
        separator = Separator('spleeter:2stems')
        # Perform the separation and get the voice file
        separator.separate_to_file(audio_path, self.cache_path)
        vocals_file_path = self.cache_path / audio_path.stem / 'vocals.wav'

        return vocals_file_path
    
    def generate_subtitles(self, video_url):
        # Extract audio from video
        print("extracting audio from video")
        raw_audio_path = self._extract_audio_from_video(video_url)

        # Extract vocals from audio
        print("extracting vocals from audio")
        audio_path = self._extract_vocals_from_audio(raw_audio_path)


        batch_size = 16 # reduce if low on GPU mem
        compute_type = "int8" # default to "float16", change to "int8" if low on GPU mem (may reduce accuracy)

        # 1. Transcribe with original whisper (batched)
        if not self.language:
          self.language = None
        model = whisperx.load_model(self.model_size, self.device, compute_type=compute_type, language=self.language)

        # save model to local path (optional)
        # model_dir = "/path/"
        # model = whisperx.load_model("large-v2", device, compute_type=compute_type, download_root=model_dir)

        audio = whisperx.load_audio(audio_path)
        result = model.transcribe(audio, batch_size=batch_size, language=self.language, chunk_size=self.subtitles_frequency)
        print("transcription before alignment: ", result["segments"]) # before alignment

        # delete model if low on GPU resources
        # import gc; gc.collect(); torch.cuda.empty_cache(); del model

        # 2. Align whisper output
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=self.device)
        result_aligned = whisperx.align(result["segments"], model_a, metadata, audio, self.device, return_char_alignments=False)

        print("transcription after alignment: ", result_aligned["segments"]) # after alignment

        # delete model if low on GPU resources
        # import gc; gc.collect(); torch.cuda.empty_cache(); del model_a

        if self.speaker_detection:
          # 3. Assign speaker labels
          diarize_model = whisperx.DiarizationPipeline(use_auth_token=self.hugging_face_token, device=self.device)

          # add min/max number of speakers if known
          diarize_segments = diarize_model(audio)
          # diarize_model(audio, min_speakers=min_speakers, max_speakers=max_speakers)

          result_aligned_with_speakers = whisperx.assign_word_speakers(diarize_segments, result_aligned)
          print("transcription after alignment with speakers: ", result_aligned_with_speakers["segments"])
          result_aligned = result_aligned_with_speakers

        result_aligned["language"] = result["language"]
        return result_aligned

    def write_subtitle_file(self, file_path: Path, result_aligned):
      with open(file_path, "w") as f:
        if file_path.suffix == ".srt":
          whisperx.utils.WriteSRT(self.captions_path).write_result(result_aligned, f, {"highlight_words": False, "max_line_width": None, "max_line_count":None})
        elif file_path.suffix == ".vtt":
          whisperx.utils.WriteVTT(self.captions_path).write_result(result_aligned, f, {"highlight_words": False, "max_line_width": None, "max_line_count":None})

    def write_subtitles(self, audio_file_path: Path, sub_format, result_aligned):
      if sub_format == "all":
        for sel_format in ['srt', 'vtt']:
          file_name = f'{audio_file_path.stem}.{sel_format}'
          file_path = os.path.join(self.captions_path, file_name)
          self.write_subtitle_file(file_path, result_aligned)
      else:
        file_name = f'{audio_file_path.stem}.{sub_format.lower()}'
        file_path = self.captions_path / file_name
        self.write_subtitle_file(file_path, result_aligned)

    def generate_subtitles_mock(self):
      time.sleep(4)
      return {'segments': [{'start': 1.099, 'end': 2.763, 'text': ' Cialo come il sole', 'words': [{'word': 'Cialo', 'start': 1.099, 'end': 1.4, 'score': 0.491}, {'word': 'come', 'start': 1.58, 'end': 1.921, 'score': 0.587}, {'word': 'il', 'start': 2.041, 'end': 2.081, 'score': 0.157}, {'word': 'sole', 'start': 2.262, 'end': 2.763, 'score': 0.559}]}, {'start': 4.238, 'end': 6.104, 'text': ' che mi scalda il cuore', 'words': [{'word': 'che', 'start': 4.238, 'end': 4.439, 'score': 0.253}, {'word': 'mi', 'start': 4.539, 'end': 4.619, 'score': 0.722}, {'word': 'scalda', 'start': 4.7, 'end': 5.302, 'score': 0.814}, {'word': 'il', 'start': 5.402, 'end': 5.462, 'score': 0.814}, {'word': 'cuore', 'start': 5.643, 'end': 6.104, 'score': 0.904}]}, {'start': 7.556, 'end': 9.306, 'text': ' e blu come il mare.', 'words': [{'word': 'e', 'start': 7.556, 'end': 7.616, 'score': 0.531}, {'word': 'blu', 'start': 7.737, 'end': 7.918, 'score': 0.709}, {'word': 'come', 'start': 8.079, 'end': 8.541, 'score': 0.774}, {'word': 'il', 'start': 8.682, 'end': 8.722, 'score': 0.255}, {'word': 'mare.', 'start': 8.803, 'end': 9.306, 'score': 0.681}]}, {'start': 10.646, 'end': 12.604, 'text': ' che sei mi consopla.', 'words': [{'word': 'che', 'start': 10.646, 'end': 10.828, 'score': 0.488}, {'word': 'sei', 'start': 10.949, 'end': 11.232, 'score': 0.777}, {'word': 'mi', 'start': 11.312, 'end': 11.454, 'score': 0.95}, {'word': 'consopla.', 'start': 11.635, 'end': 12.604, 'score': 0.918}]}, {'start': 13.844, 'end': 16.123, 'text': ' verde come campiche', 'words': [{'word': 'verde', 'start': 13.844, 'end': 14.368, 'score': 0.777}, {'word': 'come', 'start': 14.529, 'end': 14.912, 'score': 0.838}, {'word': 'campiche', 'start': 15.094, 'end': 16.123, 'score': 0.852}]}, {'start': 16.706, 'end': 18.569, 'text': ' mi ricordano casa', 'words': [{'word': 'mi', 'start': 16.706, 'end': 16.866, 'score': 0.634}, {'word': 'ricordano', 'start': 16.926, 'end': 17.828, 'score': 0.751}, {'word': 'casa', 'start': 18.068, 'end': 18.569, 'score': 0.673}]}, {'start': 20.313, 'end': 22.218, 'text': ' e quel rosso forte.', 'words': [{'word': 'e', 'start': 20.313, 'end': 20.393, 'score': 0.625}, {'word': 'quel', 'start': 20.474, 'end': 20.674, 'score': 0.688}, {'word': 'rosso', 'start': 20.754, 'end': 21.155, 'score': 0.777}, {'word': 'forte.', 'start': 21.376, 'end': 22.218, 'score': 0.83}]}, {'start': 23.478, 'end': 24.954, 'text': ' di quella stanza.', 'words': [{'word': 'di', 'start': 23.478, 'end': 23.579, 'score': 0.578}, {'word': 'quella', 'start': 23.72, 'end': 24.206, 'score': 0.652}, {'word': 'stanza.', 'start': 24.307, 'end': 24.954, 'score': 0.633}]}, {'start': 26.048, 'end': 29.108, 'text': ' e poi non parlo che se parlo non so dire basta', 'words': [{'word': 'e', 'start': 26.048, 'end': 26.088, 'score': 0.566}, {'word': 'poi', 'start': 26.209, 'end': 26.37, 'score': 0.847}, {'word': 'non', 'start': 26.41, 'end': 26.551, 'score': 0.368}, {'word': 'parlo', 'start': 26.611, 'end': 26.933, 'score': 0.861}, {'word': 'che', 'start': 26.994, 'end': 27.115, 'score': 0.838}, {'word': 'se', 'start': 27.215, 'end': 27.316, 'score': 0.835}, {'word': 'parlo', 'start': 27.437, 'end': 27.779, 'score': 0.893}, {'word': 'non', 'start': 27.839, 'end': 27.98, 'score': 0.92}, {'word': 'so', 'start': 28.061, 'end': 28.182, 'score': 0.869}, {'word': 'dire', 'start': 28.242, 'end': 28.484, 'score': 0.652}, {'word': 'basta', 'start': 28.625, 'end': 29.108, 'score': 0.912}]}, {'start': 29.45, 'end': 32.347, 'text': ' ballo o manco avessi preso lezioni di danza', 'words': [{'word': 'ballo', 'start': 29.45, 'end': 29.711, 'score': 0.727}, {'word': 'o', 'start': 29.731, 'end': 29.772, 'score': 0.585}, {'word': 'manco', 'start': 29.832, 'end': 30.114, 'score': 0.721}, {'word': 'avessi', 'start': 30.174, 'end': 30.536, 'score': 0.898}, {'word': 'preso', 'start': 30.637, 'end': 30.959, 'score': 0.972}, {'word': 'lezioni', 'start': 31.059, 'end': 31.562, 'score': 0.924}, {'word': 'di', 'start': 31.663, 'end': 31.743, 'score': 0.978}, {'word': 'danza', 'start': 31.884, 'end': 32.347, 'score': 0.975}]}, {'start': 32.909, 'end': 35.555, 'text': ' Non ho mai avuto paura di essere abbastanza', 'words': [{'word': 'Non', 'start': 32.909, 'end': 33.029, 'score': 0.83}, {'word': 'ho', 'start': 33.069, 'end': 33.169, 'score': 0.279}, {'word': 'mai', 'start': 33.19, 'end': 33.25, 'score': 0.029}, {'word': 'avuto', 'start': 33.27, 'end': 33.53, 'score': 0.686}, {'word': 'paura', 'start': 33.691, 'end': 34.192, 'score': 0.772}, {'word': 'di', 'start': 34.252, 'end': 34.332, 'score': 0.556}, {'word': 'essere', 'start': 34.352, 'end': 34.733, 'score': 0.918}, {'word': 'abbastanza', 'start': 34.794, 'end': 35.555, 'score': 0.954}]}, {'start': 36.017, 'end': 38.485, 'text': ' resto con i piedi in terra si mascalza', 'words': [{'word': 'resto', 'start': 36.017, 'end': 36.238, 'score': 0.681}, {'word': 'con', 'start': 36.318, 'end': 36.458, 'score': 0.809}, {'word': 'i', 'start': 36.519, 'end': 36.559, 'score': 0.695}, {'word': 'piedi', 'start': 36.639, 'end': 36.94, 'score': 0.62}, {'word': 'in', 'start': 36.96, 'end': 37.02, 'score': 0.871}, {'word': 'terra', 'start': 37.08, 'end': 37.381, 'score': 0.978}, {'word': 'si', 'start': 37.522, 'end': 37.662, 'score': 0.837}, {'word': 'mascalza', 'start': 37.743, 'end': 38.485, 'score': 0.904}]}, {'start': 38.927, 'end': 41.636, 'text': ' sempre in salita, tutta la vita', 'words': [{'word': 'sempre', 'start': 38.927, 'end': 39.188, 'score': 0.978}, {'word': 'in', 'start': 39.228, 'end': 39.288, 'score': 0.758}, {'word': 'salita,', 'start': 39.348, 'end': 40.331, 'score': 0.868}, {'word': 'tutta', 'start': 40.592, 'end': 40.954, 'score': 0.626}, {'word': 'la', 'start': 41.034, 'end': 41.215, 'score': 0.938}, {'word': 'vita', 'start': 41.275, 'end': 41.636, 'score': 0.918}]}, {'start': 42.178, 'end': 44.884, 'text': ' Ma mi diceva che intrappaglia lo conquista', 'words': [{'word': 'Ma', 'start': 42.178, 'end': 42.318, 'score': 0.936}, {'word': 'mi', 'start': 42.378, 'end': 42.498, 'score': 0.994}, {'word': 'diceva', 'start': 42.579, 'end': 43.04, 'score': 0.913}, {'word': 'che', 'start': 43.14, 'end': 43.22, 'score': 0.185}, {'word': 'intrappaglia', 'start': 43.26, 'end': 43.902, 'score': 0.57}, {'word': 'lo', 'start': 43.962, 'end': 44.082, 'score': 0.666}, {'word': 'conquista', 'start': 44.183, 'end': 44.884, 'score': 0.922}]}, {'start': 45.407, 'end': 46.695, 'text': " C'erco la fia e chi diria?", 'words': [{'word': "C'erco", 'start': 45.407, 'end': 45.689, 'score': 0.56}, {'word': 'la', 'start': 45.729, 'end': 45.789, 'score': 0.21}, {'word': 'fia', 'start': 45.829, 'end': 45.91, 'score': 0.167}, {'word': 'e', 'start': 45.991, 'end': 46.031, 'score': 0.432}, {'word': 'chi', 'start': 46.152, 'end': 46.212, 'score': 0.145}, {'word': 'diria?', 'start': 46.393, 'end': 46.695, 'score': 0.322}]}, {'start': 48.547, 'end': 51.764, 'text': ' un arco balleno verso la mia conquista.', 'words': [{'word': 'un', 'start': 48.547, 'end': 48.748, 'score': 0.684}, {'word': 'arco', 'start': 48.768, 'end': 48.969, 'score': 0.504}, {'word': 'balleno', 'start': 49.01, 'end': 49.573, 'score': 0.76}, {'word': 'verso', 'start': 49.653, 'end': 50.115, 'score': 0.933}, {'word': 'la', 'start': 50.276, 'end': 50.497, 'score': 0.944}, {'word': 'mia', 'start': 50.558, 'end': 50.779, 'score': 0.949}, {'word': 'conquista.', 'start': 50.96, 'end': 51.764, 'score': 0.797}]}, {'start': 54.572, 'end': 58.187, 'text': ' Su un arco baleno verso la mia conquista', 'words': [{'word': 'Su', 'start': 54.572, 'end': 54.833, 'score': 0.901}, {'word': 'un', 'start': 54.913, 'end': 54.994, 'score': 0.742}, {'word': 'arco', 'start': 55.034, 'end': 55.295, 'score': 0.837}, {'word': 'baleno', 'start': 55.375, 'end': 55.917, 'score': 0.944}, {'word': 'verso', 'start': 56.038, 'end': 56.54, 'score': 0.932}, {'word': 'la', 'start': 56.681, 'end': 56.902, 'score': 0.861}, {'word': 'mia', 'start': 56.962, 'end': 57.203, 'score': 0.816}, {'word': 'conquista', 'start': 57.324, 'end': 58.187, 'score': 0.834}]}], 'word_segments': [{'word': 'Cialo', 'start': 1.099, 'end': 1.4, 'score': 0.491}, {'word': 'come', 'start': 1.58, 'end': 1.921, 'score': 0.587}, {'word': 'il', 'start': 2.041, 'end': 2.081, 'score': 0.157}, {'word': 'sole', 'start': 2.262, 'end': 2.763, 'score': 0.559}, {'word': 'che', 'start': 4.238, 'end': 4.439, 'score': 0.253}, {'word': 'mi', 'start': 4.539, 'end': 4.619, 'score': 0.722}, {'word': 'scalda', 'start': 4.7, 'end': 5.302, 'score': 0.814}, {'word': 'il', 'start': 5.402, 'end': 5.462, 'score': 0.814}, {'word': 'cuore', 'start': 5.643, 'end': 6.104, 'score': 0.904}, {'word': 'e', 'start': 7.556, 'end': 7.616, 'score': 0.531}, {'word': 'blu', 'start': 7.737, 'end': 7.918, 'score': 0.709}, {'word': 'come', 'start': 8.079, 'end': 8.541, 'score': 0.774}, {'word': 'il', 'start': 8.682, 'end': 8.722, 'score': 0.255}, {'word': 'mare.', 'start': 8.803, 'end': 9.306, 'score': 0.681}, {'word': 'che', 'start': 10.646, 'end': 10.828, 'score': 0.488}, {'word': 'sei', 'start': 10.949, 'end': 11.232, 'score': 0.777}, {'word': 'mi', 'start': 11.312, 'end': 11.454, 'score': 0.95}, {'word': 'consopla.', 'start': 11.635, 'end': 12.604, 'score': 0.918}, {'word': 'verde', 'start': 13.844, 'end': 14.368, 'score': 0.777}, {'word': 'come', 'start': 14.529, 'end': 14.912, 'score': 0.838}, {'word': 'campiche', 'start': 15.094, 'end': 16.123, 'score': 0.852}, {'word': 'mi', 'start': 16.706, 'end': 16.866, 'score': 0.634}, {'word': 'ricordano', 'start': 16.926, 'end': 17.828, 'score': 0.751}, {'word': 'casa', 'start': 18.068, 'end': 18.569, 'score': 0.673}, {'word': 'e', 'start': 20.313, 'end': 20.393, 'score': 0.625}, {'word': 'quel', 'start': 20.474, 'end': 20.674, 'score': 0.688}, {'word': 'rosso', 'start': 20.754, 'end': 21.155, 'score': 0.777}, {'word': 'forte.', 'start': 21.376, 'end': 22.218, 'score': 0.83}, {'word': 'di', 'start': 23.478, 'end': 23.579, 'score': 0.578}, {'word': 'quella', 'start': 23.72, 'end': 24.206, 'score': 0.652}, {'word': 'stanza.', 'start': 24.307, 'end': 24.954, 'score': 0.633}, {'word': 'e', 'start': 26.048, 'end': 26.088, 'score': 0.566}, {'word': 'poi', 'start': 26.209, 'end': 26.37, 'score': 0.847}, {'word': 'non', 'start': 26.41, 'end': 26.551, 'score': 0.368}, {'word': 'parlo', 'start': 26.611, 'end': 26.933, 'score': 0.861}, {'word': 'che', 'start': 26.994, 'end': 27.115, 'score': 0.838}, {'word': 'se', 'start': 27.215, 'end': 27.316, 'score': 0.835}, {'word': 'parlo', 'start': 27.437, 'end': 27.779, 'score': 0.893}, {'word': 'non', 'start': 27.839, 'end': 27.98, 'score': 0.92}, {'word': 'so', 'start': 28.061, 'end': 28.182, 'score': 0.869}, {'word': 'dire', 'start': 28.242, 'end': 28.484, 'score': 0.652}, {'word': 'basta', 'start': 28.625, 'end': 29.108, 'score': 0.912}, {'word': 'ballo', 'start': 29.45, 'end': 29.711, 'score': 0.727}, {'word': 'o', 'start': 29.731, 'end': 29.772, 'score': 0.585}, {'word': 'manco', 'start': 29.832, 'end': 30.114, 'score': 0.721}, {'word': 'avessi', 'start': 30.174, 'end': 30.536, 'score': 0.898}, {'word': 'preso', 'start': 30.637, 'end': 30.959, 'score': 0.972}, {'word': 'lezioni', 'start': 31.059, 'end': 31.562, 'score': 0.924}, {'word': 'di', 'start': 31.663, 'end': 31.743, 'score': 0.978}, {'word': 'danza', 'start': 31.884, 'end': 32.347, 'score': 0.975}, {'word': 'Non', 'start': 32.909, 'end': 33.029, 'score': 0.83}, {'word': 'ho', 'start': 33.069, 'end': 33.169, 'score': 0.279}, {'word': 'mai', 'start': 33.19, 'end': 33.25, 'score': 0.029}, {'word': 'avuto', 'start': 33.27, 'end': 33.53, 'score': 0.686}, {'word': 'paura', 'start': 33.691, 'end': 34.192, 'score': 0.772}, {'word': 'di', 'start': 34.252, 'end': 34.332, 'score': 0.556}, {'word': 'essere', 'start': 34.352, 'end': 34.733, 'score': 0.918}, {'word': 'abbastanza', 'start': 34.794, 'end': 35.555, 'score': 0.954}, {'word': 'resto', 'start': 36.017, 'end': 36.238, 'score': 0.681}, {'word': 'con', 'start': 36.318, 'end': 36.458, 'score': 0.809}, {'word': 'i', 'start': 36.519, 'end': 36.559, 'score': 0.695}, {'word': 'piedi', 'start': 36.639, 'end': 36.94, 'score': 0.62}, {'word': 'in', 'start': 36.96, 'end': 37.02, 'score': 0.871}, {'word': 'terra', 'start': 37.08, 'end': 37.381, 'score': 0.978}, {'word': 'si', 'start': 37.522, 'end': 37.662, 'score': 0.837}, {'word': 'mascalza', 'start': 37.743, 'end': 38.485, 'score': 0.904}, {'word': 'sempre', 'start': 38.927, 'end': 39.188, 'score': 0.978}, {'word': 'in', 'start': 39.228, 'end': 39.288, 'score': 0.758}, {'word': 'salita,', 'start': 39.348, 'end': 40.331, 'score': 0.868}, {'word': 'tutta', 'start': 40.592, 'end': 40.954, 'score': 0.626}, {'word': 'la', 'start': 41.034, 'end': 41.215, 'score': 0.938}, {'word': 'vita', 'start': 41.275, 'end': 41.636, 'score': 0.918}, {'word': 'Ma', 'start': 42.178, 'end': 42.318, 'score': 0.936}, {'word': 'mi', 'start': 42.378, 'end': 42.498, 'score': 0.994}, {'word': 'diceva', 'start': 42.579, 'end': 43.04, 'score': 0.913}, {'word': 'che', 'start': 43.14, 'end': 43.22, 'score': 0.185}, {'word': 'intrappaglia', 'start': 43.26, 'end': 43.902, 'score': 0.57}, {'word': 'lo', 'start': 43.962, 'end': 44.082, 'score': 0.666}, {'word': 'conquista', 'start': 44.183, 'end': 44.884, 'score': 0.922}, {'word': "C'erco", 'start': 45.407, 'end': 45.689, 'score': 0.56}, {'word': 'la', 'start': 45.729, 'end': 45.789, 'score': 0.21}, {'word': 'fia', 'start': 45.829, 'end': 45.91, 'score': 0.167}, {'word': 'e', 'start': 45.991, 'end': 46.031, 'score': 0.432}, {'word': 'chi', 'start': 46.152, 'end': 46.212, 'score': 0.145}, {'word': 'diria?', 'start': 46.393, 'end': 46.695, 'score': 0.322}, {'word': 'un', 'start': 48.547, 'end': 48.748, 'score': 0.684}, {'word': 'arco', 'start': 48.768, 'end': 48.969, 'score': 0.504}, {'word': 'balleno', 'start': 49.01, 'end': 49.573, 'score': 0.76}, {'word': 'verso', 'start': 49.653, 'end': 50.115, 'score': 0.933}, {'word': 'la', 'start': 50.276, 'end': 50.497, 'score': 0.944}, {'word': 'mia', 'start': 50.558, 'end': 50.779, 'score': 0.949}, {'word': 'conquista.', 'start': 50.96, 'end': 51.764, 'score': 0.797}, {'word': 'Su', 'start': 54.572, 'end': 54.833, 'score': 0.901}, {'word': 'un', 'start': 54.913, 'end': 54.994, 'score': 0.742}, {'word': 'arco', 'start': 55.034, 'end': 55.295, 'score': 0.837}, {'word': 'baleno', 'start': 55.375, 'end': 55.917, 'score': 0.944}, {'word': 'verso', 'start': 56.038, 'end': 56.54, 'score': 0.932}, {'word': 'la', 'start': 56.681, 'end': 56.902, 'score': 0.861}, {'word': 'mia', 'start': 56.962, 'end': 57.203, 'score': 0.816}, {'word': 'conquista', 'start': 57.324, 'end': 58.187, 'score': 0.834}], 'language': 'it'}
