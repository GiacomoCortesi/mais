"use client";

import { useState } from "react";
import { AiOutlineExport } from "react-icons/ai";
import { Button } from "@nextui-org/button";
import {
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
} from "@nextui-org/dropdown";

import Snackbar from "@/components/snackbar";
import { ChevronDownIcon } from "@/components/icons";

interface Props {
  transcriptionId: string;
}

export default function MagicButtonExport({ transcriptionId }: Props) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedOption, setSelectedOption] = useState(new Set(["srt"]));
  const [snackbarOpen, setSnackbarOpen] = useState(false);

  const onClick = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/transcription/${transcriptionId}/export?format=${selectedOptionValue}`,
      );
      const filename = `${transcriptionId}-${selectedOptionValue}`;

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");

        a.href = url;
        a.download = filename; // Set the file name
        document.body.appendChild(a);
        a.click();
        a.remove();
      } else {
        setError(await response.text());
      }
    } catch (err: unknown) {
      setError("Unexpected error in API call");
      setSnackbarOpen(true);
    } finally {
      setLoading(false);
    }
  };

  const descriptionsMap = {
    srt: "Export subtitles in srt format",
    vtt: "Export subtitles in vtt format",
    video: "Export video file with subtitles",
  };

  const labelsMap: { [key: string]: string } = {
    srt: "srt",
    vtt: "vtt",
    video: "video",
  };

  // Convert the Set to an Array and get the first value.
  const selectedOptionValue = Array.from(selectedOption)[0];

  return (
    <>
      <Button color="primary" isLoading={loading} onClick={onClick}>
        <AiOutlineExport />
        EXPORT {labelsMap[selectedOptionValue]}
      </Button>
      <Dropdown placement="bottom-end">
        <DropdownTrigger>
          <Button isIconOnly color="primary">
            <ChevronDownIcon />
          </Button>
        </DropdownTrigger>
        <DropdownMenu
          disallowEmptySelection
          aria-label="Export options"
          className="max-w-[300px]"
          selectedKeys={selectedOption}
          selectionMode="single"
          onSelectionChange={setSelectedOption}
        >
          <DropdownItem key="srt" description={descriptionsMap["srt"]}>
            {labelsMap["srt"]}
          </DropdownItem>
          <DropdownItem key="vtt" description={descriptionsMap["vtt"]}>
            {labelsMap["vtt"]}
          </DropdownItem>
          <DropdownItem key="video" description={descriptionsMap["video"]}>
            {labelsMap["video"]}
          </DropdownItem>
        </DropdownMenu>
      </Dropdown>
      <Snackbar
        isOpen={snackbarOpen}
        message={`Export failed: ${error}`}
        onClose={() => setSnackbarOpen(false)}
      />
    </>
  );
}
