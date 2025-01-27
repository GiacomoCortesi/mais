import UploadedFiles from "./uploaded-files";

export default async function UploadedFilesGrid() {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/file`, {});

  if (!response.ok) {
    throw new Error("failed to fetch uploaded video files");
  }

  const uploaded_video_files = await response.json();

  return (
    <>
      <p className="text-lg">Uploaded files:</p>
      <div className="flex items-center justify-center w-full min-h-52">
        {uploaded_video_files.length ? (
          <div className="grid gap-1 overflow-y-auto min-h-[50px] m-2 rounded-large border-opacity-50 border-white auto-cols-[8rem] grid-flow-col ">
            <UploadedFiles uploaded_video_files={uploaded_video_files} />
          </div>
        ) : (
          <p>No file uploaded</p>
        )}
      </div>
    </>
  );
}
