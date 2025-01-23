import { title } from "@/components/primitives";
import Converter from "@/components/converter/converter";
import VideoPlayer from "@/components/editor/video-player";

interface Props {
  searchParams: {
    selectedVideo?: string;
  };
}
export default function ConverterPage({ searchParams }: Props) {
  const selectedVideo =
    searchParams && searchParams["selectedVideo"]
      ? searchParams["selectedVideo"]
      : "";

  return (
    <>
      <h1 className={title()}>MAIS Converter</h1>
      <p className="text-lg">
        Instantly create and edit subtitles from a music video or audio
      </p>
      <Converter videoFile={selectedVideo} />
    </>
  );
}
