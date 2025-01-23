export interface ISubtitleJobOptions {
  speaker_detection: boolean;
  subtitles_frequency: number;
  language: string;
  model_size: string;
}

export interface ISubtitleJobConfig {
  config: ISubtitleJobOptions;
  filename: string;
}

export interface ISubtitleJobRequest {
  id?: string;
  info?: ISubtitleJobConfig;
}