import { ISegment } from "@/types/transcription";
import { SubtitleConfig } from "./subitle-config";
import VideoPlayer from "./video-player";
import { ISubtitleConfig } from "@/types/video";

interface Props {
    segments: ISegment[];
    filename: string;
    subtitleConfig: ISubtitleConfig;
    setSubtitleConfig: (value: any) => void;
}

export const VideoPreview = ({segments, filename, subtitleConfig, setSubtitleConfig}: Props) => { 
    return (
        <div>
          <SubtitleConfig
            subtitleConfig={subtitleConfig}
            setSubtitleConfig={setSubtitleConfig} 
          />
          <VideoPlayer
            subtitleConfig={subtitleConfig}
            segments={segments}
            src={`${process.env.NEXT_PUBLIC_API_URL}/file/${filename}`}
          />
        </div>
    );
}