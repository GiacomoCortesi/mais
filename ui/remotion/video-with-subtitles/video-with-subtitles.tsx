import { AbsoluteFill, Video, Sequence } from "remotion";

import { IVideoWithSubtitlesProps } from "@/types/video";

export const VideoWithSubtitles = ({
  src,
  segments,
  fps,
  subtitleConfig,
}: IVideoWithSubtitlesProps) => {
  return (
    <AbsoluteFill>
      {src && <Video src={src} />}
      {segments.map((segment, index) => (
        <Sequence
          key={index}
          durationInFrames={segment.end * fps - segment.start * fps}
          from={segment.start * fps}
        >
          <div
            style={{
              fontFamily: `${subtitleConfig?.font}`,
              position: "absolute",
              bottom: `${subtitleConfig?.position}%`,
              width: "100%",
              textAlign: "center",
              fontSize:  `${subtitleConfig?.size}px`,
              color: `${subtitleConfig?.color}`,
              // textShadow: "2px 2px 4px rgba(0, 0, 0, 0.7)",
            }}
          >
            {segment.text}
          </div>
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
