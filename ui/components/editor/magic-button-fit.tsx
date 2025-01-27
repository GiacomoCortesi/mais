"use client";
import { Button } from "@heroui/button";
import { AiOutlineAlignCenter } from "react-icons/ai";
import { useState } from "react";

import { fitTranscription } from "@/actions/transcription";

interface Props {
  transcriptionId: string;
}

export default function MagicButtonFit({ transcriptionId }: Props) {
  const [isLoading, setIsLoading] = useState(false);
  const onClick = async () => {
    setIsLoading(true);
    await fitTranscriptionWithId();
    setIsLoading(false);
  };

  const fitTranscriptionWithId = fitTranscription.bind(null, transcriptionId);

  return (
    <Button
      color="primary"
      isLoading={isLoading}
      onClick={() => {
        onClick();
      }}
    >
      <AiOutlineAlignCenter />
      FIT
    </Button>
  );
}
