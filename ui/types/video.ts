import { ISegment } from "./transcription";

export interface IVideoFile {
  id: string;
  filename: string;
  image_url: string;
}

export interface IVideoWithSubtitlesProps {
  src: string;
  segments: ISegment[];
  fps: number;
}
