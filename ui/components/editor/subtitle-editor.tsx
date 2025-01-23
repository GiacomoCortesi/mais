"use client";

import React, { ChangeEvent } from "react";
import { useState, useEffect } from "react";
import { Button } from "@heroui/button";
import { Tooltip } from "@heroui/tooltip";
import { AiOutlinePlusCircle } from "react-icons/ai";

import { ISegment, IWord } from "@/types/transcription";
import SubtitleSegment from "@/components/editor/subtitle-segment";
import { editTranscription } from "@/actions/transcription";

import MagicButtons from "./magic-buttons";
import VideoPlayer from "./video-player";

interface Props {
  language: string;
  defaultSegments: ISegment[];
  wordSegments: IWord[];
  transcriptionId: string;
  filename: string;
}

export default function SubtitleEditor({
  language,
  defaultSegments,
  wordSegments,
  transcriptionId,
  filename,
}: Props) {
  const [segments, setSegments] = useState<ISegment[]>(defaultSegments);

  // update subtitle segments everytime the defaultSegments props change (e.g. due to a Clear magic button click)
  useEffect(() => {
    const updateSegmentsOnPropsChange = () => {
      setSegments(defaultSegments);
    };

    updateSegmentsOnPropsChange();
  }, [defaultSegments]);

  const onTextHandler = (
    event: ChangeEvent<HTMLTextAreaElement>,
    index: number
  ) => {
    const newSegments = [...segments];

    newSegments[index].text = event.target.value;
    setSegments(newSegments);
  };
  const onStartHandler = (
    event: ChangeEvent<HTMLInputElement>,
    index: number
  ) => {
    const newSegments = [...segments];

    newSegments[index].start = Number(event.target.value);

    setSegments(newSegments);
  };
  const onEndHandler = (
    event: ChangeEvent<HTMLInputElement>,
    index: number
  ) => {
    let value = Number(event.target.value);

    if (value < 0) {
      value = 0;
    }

    console.log(value);

    const newSegments = [...segments];

    newSegments[index].end = Number(value);
    setSegments(newSegments);
  };
  const onDeleteHandler = (index: number) => {
    const newSegments = [...segments];

    newSegments.splice(index, 1);
    setSegments(newSegments);
  };

  const handleAddSegment = (index: number) => {
    const newSegments = [...segments];

    const segment: ISegment = {
      words: [],
      start: segments[index].start,
      end: segments[index].end,
      text: "",
    };

    newSegments.splice(index, 0, segment);
    setSegments(newSegments);
  };

  return (
    <div className="flex flex-col gap-4">
      <VideoPlayer
        segments={segments}
        src={`${process.env.NEXT_PUBLIC_API_URL}/file/${filename}`}
      />
      <Button
        className="my-2"
        color="secondary"
        onClick={editTranscription.bind(null, transcriptionId, {
          language: language,
          segments: segments,
          word_segments: wordSegments,
        })}
      >
        SAVE
      </Button>
      {<p className="text-lg">Language: {language}</p>}
      {segments.map((segment: ISegment, index: number) => {
        return (
          <>
            <div key={`add-btn-cnt-${index}`} className="flex justify-center">
              <Tooltip content="Add empty subtitle segment" delay={1000}>
                <Button
                  isIconOnly
                  className="w-5 h-5"
                  color="secondary"
                  variant="light"
                  onClick={(_) => handleAddSegment(index)}
                >
                  <AiOutlinePlusCircle className="w-full h-full" />
                </Button>
              </Tooltip>
            </div>
            <SubtitleSegment
              key={`segment-${index}`}
              end={segment.end}
              start={segment.start}
              text={segment.text}
              onDelete={() => onDeleteHandler(index)}
              onEnd={(event: ChangeEvent<HTMLInputElement>) =>
                onEndHandler(event, index)
              }
              onStart={(event: ChangeEvent<HTMLInputElement>) =>
                onStartHandler(event, index)
              }
              onText={(event: ChangeEvent<HTMLTextAreaElement>) =>
                onTextHandler(event, index)
              }
            />
          </>
        );
      })}
      <MagicButtons transcriptionId={transcriptionId} />
    </div>
  );
}
