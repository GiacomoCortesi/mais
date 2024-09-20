export const dynamic = "force-dynamic";
import TranscriptionTable from "@/components/transcription-table";
import { ITranscription } from "@/types/transcription";
export default async function EditorPage() {
  const response = await fetch(`${process.env.API_URL}/transcription`);

  if (!response.ok) {
    throw new Error("failed to fetch transcription");
  }

  const transcriptions: ITranscription[] = await response.json();

  return (
    <>
      <p className={"text-4xl my-4"}>Subtitle Transcriptions</p>
      <TranscriptionTable transcriptions={transcriptions} />
    </>
  );
}
