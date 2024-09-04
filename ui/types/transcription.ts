export interface ITranscription {
  transcription_id: "string";
  data: ITranscriptionData;
  job_id: "string";
  video_file: "string";
}

export interface ITranscriptionData {
  segments: ISegment[];
  word_segments: IWord[];
  language: string;
}

export interface ISegment {
  start: number;
  end: number;
  text: string;
  words: IWord[];
}

export interface IWord {
  word: string;
  start: number;
  end: number;
  score: number;
}
