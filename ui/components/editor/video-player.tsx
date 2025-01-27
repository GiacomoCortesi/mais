"use client";
import { Player } from "@remotion/player";
import { getVideoMetadata } from "@remotion/media-utils";
import { useEffect, useState } from "react";

import { ISegment } from "@/types/transcription";

import { VideoWithSubtitles } from "../../remotion/video-with-subtitles/video-with-subtitles";
import { ISubtitleConfig } from "@/types/video";

interface Props {
  src: string;
  segments: ISegment[];
  subtitleConfig: ISubtitleConfig
}

export default function VideoPlayer({ src, segments, subtitleConfig }: Props) {
  const [compositionWidth, setCompositionWidth] = useState<number>(1080);
  const [compositionHeight, setCompositionHeight] = useState<number>(1920);

  useEffect(() => {
    getVideoMetadata(src)
      .then(({ width, height }) => {
        setCompositionWidth(width);
        setCompositionHeight(height);
        console.log("width ", width, "height ", height);
      })
      .catch((err) => {
        console.log(`Error fetching metadata: ${err}`);
      });
  }, []);

  const fps = 30;

  return (
    <div className="my-2">
      <Player
        compositionHeight={compositionHeight}
        compositionWidth={compositionWidth}
        controls={true}
        fps={fps}
        showVolumeControls={true}
        inputProps={{ src: src, segments: segments, fps, subtitleConfig }}
        durationInFrames={Math.ceil(segments[segments.length - 1].end * 30)}
        style={{ margin: "auto", height: 500 }}
        // eslint-disable-next-line jsx-a11y/media-has-caption
        component={VideoWithSubtitles}
      />
    </div>
  );
}
