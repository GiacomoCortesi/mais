import { ITranscription, ITranscriptionData } from "@/types/transcription";

import {
  revalidateTranscription,
  revalidateTranscriptions,
} from "./revalidateActions";

export async function createTranscription(
  transcription: string,
  jobId: string,
  videoFile: string,
) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/transcription`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      data: transcription,
      job_id: jobId,
      filename: videoFile,
    }),
  });

  if (!res.ok) throw new Error(await res.text());

  const data = await res.json();

  return data;
}

export async function clearTranscription(transcriptionId: string) {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/transcription/${transcriptionId}/clear`,
    {
      method: "POST",
    },
  );

  if (!res.ok) throw new Error(await res.text());
  revalidateTranscription(transcriptionId);
}

export async function fitTranscription(transcriptionId: string) {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/transcription/${transcriptionId}/fit`,
    {
      method: "POST",
    },
  );

  if (!res.ok) throw new Error(await res.text());
  revalidateTranscription(transcriptionId);
}

export async function fixTranscription(transcriptionId: string) {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/transcription/${transcriptionId}/fix`,
    {
      method: "POST",
    },
  );

  if (!res.ok) throw new Error(await res.text());
  revalidateTranscription(transcriptionId);
}

export async function editTranscription(
  transcriptionId: string,
  transcription: ITranscription,
) {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/transcription/${transcriptionId}`,
    {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(transcription),
    },
  );

  if (!res.ok) throw new Error(await res.text());

  revalidateTranscription(transcriptionId);
}

export async function deleteTranscription(transcriptionId: string) {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/transcription/${transcriptionId}`,
    {
      method: "DELETE",
    },
  );

  if (!res.ok) throw new Error(await res.text());
  revalidateTranscriptions();
}
