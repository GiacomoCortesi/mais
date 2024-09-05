/* eslint-disable jsx-a11y/label-has-associated-control */
"use client";

import { ChangeEvent } from "react";

import { revalidateVideoFiles } from "@/actions/revalidateActions";
import { useRouter, usePathname } from "next/navigation";
import { useState } from "react";

export default function FileUpload() {
  const router = useRouter();
  const pathName = usePathname();

  const [isDragging, setIsDragging] = useState(false);

  const handleFileChange = async (event: ChangeEvent<HTMLInputElement>) => {
    if (!event.target.files) return;

    const selectedFile = event.target.files[0];

    const data = new FormData();

    data.set("file", selectedFile);

    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/video`, {
      method: "POST",
      body: data,
    });

    if (!res.ok) throw new Error(await res.text());

    revalidateVideoFiles();

    // Update the URL's search parameters
    const newSearchParams = new URLSearchParams();

    newSearchParams.set("selectedVideo", selectedFile.name);
    router.push(`${pathName}?${newSearchParams.toString()}`);
  };

  const handleDragEnter = () => {
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  return (
    <div className="flex w-full items-center justify-center m-2">
      <label
        className={`${isDragging && "dark:border-purple-500 dark:bg-gray-900 bg-gray-100"} flex flex-col items-center justify-center w-full h-64 border-3 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-gray-900 dark:bg-gray-800 hover:bg-gray-100 dark:border-purple-600 dark:hover:border-purple-500`}
        htmlFor="dropzone-file"
      >
        <div className="absolute">
          <svg
            className="mx-auto w-8 h-8 mb-4 text-gray-500 dark:text-gray-400"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 20 16"
          >
            <path
              stroke="currentColor"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
            />
          </svg>
          <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
            <span className="font-semibold">Click to upload</span> or drag and
            drop
          </p>
          <p className="text-xs text-gray-500 dark:text-gray-400">M4A, MOV</p>
        </div>
        <input
          onDragEnter={handleDragEnter}
          onDragLeave={handleDragLeave}
          onChange={handleFileChange}
          id="dropzone-file"
          type="file"
          className="opacity-0 w-full h-full"
        />
      </label>
    </div>
  );
}
