"use client";
import { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import { useSearchParams } from "next/navigation";

import { IVideoFile } from "@/types/video";

import PreviewImageCard from "./preview-image-card";

export interface Props {
  uploaded_video_files: IVideoFile[];
}

export default function UploadedFiles({ uploaded_video_files }: Props) {
  const searchParams = useSearchParams();

  const [selectedVideo, setSelectedVideo] = useState("");
  const router = useRouter();
  const pathName = usePathname();

  useEffect(() => {
    const selectedVideoQP = searchParams.get("selectedVideo");

    if (selectedVideoQP) {
      setSelectedVideo(selectedVideoQP);
    }
  }, [uploaded_video_files]);

  const onSelectVideo = (video: string) => {
    setSelectedVideo(video);
    // Update the URL's search parameters
    const newSearchParams = new URLSearchParams();

    newSearchParams.set("selectedVideo", video);
    router.push(`${pathName}?${newSearchParams.toString()}`);
  };

  return (
    <>
      {uploaded_video_files.length &&
        uploaded_video_files.map((uploaded_video_file) => {
          return (
            <PreviewImageCard
              key={uploaded_video_file.id}
              alt={uploaded_video_file.filename}
              isSelected={uploaded_video_file.filename === selectedVideo}
              src={uploaded_video_file.image_url}
              onSelectVideo={onSelectVideo}
            />
          );
        })}
    </>
  );
}
