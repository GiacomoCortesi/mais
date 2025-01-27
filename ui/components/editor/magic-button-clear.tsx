"use client";

import { Button } from "@heroui/button";
import { AiOutlineClear } from "react-icons/ai";
import { useState } from "react";

import { clearTranscription } from "@/actions/transcription";

interface Props {
  transcriptionId: string;
}

export default function MagicButtonClear({ transcriptionId }: Props) {
  const [isLoading, setIsLoading] = useState(false);

  const onClick = async () => {
    setIsLoading(true);
    await clearTranscriptionWithId();
    setIsLoading(false);
  };
  const clearTranscriptionWithId = clearTranscription.bind(
    null,
    transcriptionId,
  );

  return (
    <Button color="primary" isLoading={isLoading} onClick={onClick}>
      <AiOutlineClear />
      CLEAR
    </Button>
  );
}
