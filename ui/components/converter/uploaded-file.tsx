"use client";

import { IFile } from "@/types/file";

import PreviewImageCard from "./preview-image-card";

export interface Props {
  uploadedFile: IFile;
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
