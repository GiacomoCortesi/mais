import { revalidateVideoFiles } from "./revalidateActions";

export async function deleteFile(filename: string) {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/file?filename=${filename}`,
    {
      method: "DELETE",
    },
  );

  if (!res.ok) throw new Error(await res.text());

  revalidateVideoFiles();
}

export async function uploadFile(formData: FormData) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/file`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error(await res.text());

  revalidateVideoFiles();
}
