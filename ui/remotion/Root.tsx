import { Composition } from "remotion";

import { IVideoWithSubtitlesProps } from "@/types/video";

import { VideoWithSubtitles } from "./video-with-subtitles/video-with-subtitles";

export const COMP_NAME = "MusicAISubComposition";

export const defaultCompProps: IVideoWithSubtitlesProps = {
  src: "",
  segments: [],
  fps: 30,
  width: 1080,
  height: 1920,
  duration: 0,
  subtitleConfig: {
    font: "Arial",
    size: 30,
    color: "#ffffff",
    position: 90,
  },
};

export const DURATION_IN_FRAMES = 200;
export const VIDEO_WIDTH = 1080;
export const VIDEO_HEIGHT = 1920;
export const VIDEO_FPS = 30;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        /* TODO: FIX TYPING HERE */
        component={VideoWithSubtitles as unknown as React.FC<Record<string, unknown>>}
        defaultProps={defaultCompProps}
        durationInFrames={DURATION_IN_FRAMES}
        fps={VIDEO_FPS}
        calculateMetadata={async ({props}) => {
          // uncomment to get metadata from video src
          // const {slowDurationInSeconds, dimensions, fps} = await parseMedia({
          //   src: props.src as string,
          //   fields: {slowDurationInSeconds: true, dimensions: true, fps: true},
          // });

          // override default props with input props
          return {
            durationInFrames: Math.floor(props?.duration as number * 30) || DURATION_IN_FRAMES,
            width: props?.width as number || VIDEO_WIDTH,
            height: props?.height as number || VIDEO_HEIGHT,
            fps: props?.fps as number || VIDEO_FPS,
          };
        }}
        height={VIDEO_HEIGHT}
        id={COMP_NAME}
        width={VIDEO_WIDTH}
      />
    </>
  );
};
