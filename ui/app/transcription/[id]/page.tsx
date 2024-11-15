import { title } from "@/components/primitives";
import SubtitleEditor from "@/components/editor/subtitle-editor";
import { ITranscription } from "@/types/transcription";

export default async function Page({ params }: { params: { id: string } }) {
  const response = await fetch(
    `${process.env.API_URL}/transcription/${params.id}`,
    {
      method: "GET",
      cache: "no-store",
    }
  );

  if (!response.ok) {
    throw new Error("failed to fetch transcription");
  }

  const transcription: ITranscription = await response.json();
  return (
    <div>
      <h1 className={title()}>MAIS Editor</h1>
      <SubtitleEditor
        defaultSegments={transcription.data.segments}
        language={transcription.data.language}
        transcriptionId={transcription.id}
        wordSegments={transcription.data.word_segments}
        filename={transcription.filename}
      />
    </div>
  );
}
