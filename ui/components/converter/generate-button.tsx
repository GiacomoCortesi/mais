"use client";
import { useState } from "react";
import { Button, ButtonGroup } from "@heroui/button";

import startJob from "@/actions/job";
import { ISubtitleJobOptions } from "@/types/job";

import JobStatus from "./job-status-card";
import SettingsDropdown from "./settings-dropdown";

export interface Props {
  videoFile: string;
}

export default function GenerateButton({ videoFile }: Props) {
  const [jobId, setJobId] = useState("");
  const [isRunning, setIsRunning] = useState(false);
  const [options, setOptions] = useState<ISubtitleJobOptions>({
    speaker_detection: true,
    subtitles_frequency: 5,
    language: "it",
    model_size: "medium",
  });

  const onStatusChange = (newStatus: string) => {
    if (newStatus == "pending") {
      setIsRunning(true);
    }
    if (newStatus === "completed" || newStatus == "failed") {
      setIsRunning(false);
    }
  };

  const onClick = async () => {
    const { id } = await startJob(videoFile, options);

    setIsRunning(true);
    setJobId(id);
  };

  const updateOptions = (key: string, value: any) => {
    setOptions((prevParams) => ({
      ...prevParams,
      [key]: value,
    }));
  };

  return (
    <>
      <ButtonGroup>
        <Button
          isDisabled={videoFile ? false : true}
          isLoading={isRunning ? true : false}
          onClick={() => onClick()}
        >
          {videoFile ? "Generate" : "Select video"}
        </Button>
        <SettingsDropdown
          isDisabled={jobId ? true : false}
          options={options}
          onOptionUpdate={updateOptions}
        />
      </ButtonGroup>
      {isRunning && <JobStatus jobId={jobId} onStatusChange={onStatusChange} />}
    </>
  );
}
