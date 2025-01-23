import { Composition } from "remotion";

import { IVideoWithSubtitlesProps } from "@/types/video";

import { VideoWithSubtitles } from "./video-with-subtitles/video-with-subtitles";

export const COMP_NAME = "MusicAISubComposition";

export const defaultCompProps: IVideoWithSubtitlesProps = {
  src: "",
  segments: [],
  fps: 30,
};

export const DURATION_IN_FRAMES = 200;
export const VIDEO_WIDTH = 1080;
export const VIDEO_HEIGHT = 1920;
export const VIDEO_FPS = 30;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        component={VideoWithSubtitles}
        defaultProps={defaultCompProps}
        durationInFrames={DURATION_IN_FRAMES}
        fps={VIDEO_FPS}
        height={VIDEO_HEIGHT}
        id={COMP_NAME}
        width={VIDEO_WIDTH}
      />
    </>
  );
};
