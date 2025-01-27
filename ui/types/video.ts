import { ISegment } from "./transcription";

export interface IFile {
  id: string;
  filename: string;
  image_url: string;
}

export interface IVideoWithSubtitlesProps {
  src: string;
  segments: ISegment[];
  fps: number;
  width: number;
  height: number;
  duration: number;
  subtitleConfig: ISubtitleConfig
}

export interface ISubtitleConfig {
  position: number;
  color: string;
  size: number;
  font: string;
}

