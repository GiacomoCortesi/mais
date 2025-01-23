"use client";
import { AiOutlineTool } from "react-icons/ai";
import { Button } from "@heroui/button";
import { useState } from "react";

import { fixTranscription } from "@/actions/transcription";

interface Props {
  transcriptionId: string;
}

export default function MagicButtonFix({ transcriptionId }: Props) {
  const [isLoading, setIsLoading] = useState(false);

  const onClick = async () => {
    setIsLoading(true);
    await fixTranscriptionWithId();
    setIsLoading(false);
  };

  const fixTranscriptionWithId = fixTranscription.bind(null, transcriptionId);

  return (
    <Button
      color="primary"
      isLoading={isLoading}
      onClick={() => {
        onClick();
      }}
    >
      <AiOutlineTool />
      FIX
    </Button>
  );
}
