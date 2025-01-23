"use client";

import { IVideoFile } from "@/types/video";

import PreviewImageCard from "./preview-image-card";

export interface Props {
  uploadedFile: IVideoFile;
}

export default function UploadedFile({ uploadedFile }: Props) {
  return (
    <>
      <div className="min-w-32 max-w-52">
        {uploadedFile ? (
          <PreviewImageCard
            isSelected
            alt={uploadedFile.filename}
            src={uploadedFile.image_url}
            onSelectVideo={(_: string) => {}}
          />
        ) : (
          <p>No file uploaded</p>
        )}
      </div>
    </>
  );
}
