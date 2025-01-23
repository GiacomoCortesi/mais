import { ISubtitleJobOptions } from "@/types/job";

export default async function startJob(
  filename: string,
  options: ISubtitleJobOptions,
) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/job`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({info: { filename: filename, config: options }}),
  });

  if (!res.ok) throw new Error(await res.text());

  const data = await res.json();

  return data;
}
