"use client";

import React, { ChangeEventHandler, MouseEventHandler } from "react";
import { Card, CardBody, CardHeader } from "@heroui/card";
import { Textarea } from "@heroui/input";
import { AiFillCloseCircle } from "react-icons/ai";
import { Tooltip } from "@heroui/tooltip";

import SubtitleSegmentCounter from "./subtitle-segment-counter";

interface Props {
  start: number;
  end: number;
  text: string;
  onStart: ChangeEventHandler;
  onEnd: ChangeEventHandler;
  onText: ChangeEventHandler;
  onDelete: MouseEventHandler;
}
export default function SubtitleSegment({
  start,
  end,
  text,
  onStart,
  onEnd,
  onText,
  onDelete,
}: Props) {
  return (
    <Card>
      {
        <CardHeader className="flex gap-3">
          <Tooltip content="Delete subtitle segment" delay={1000}>
            <button
              className="absolute top-0 right-0 m-1 z-10 focus:outline-none"
              onClick={onDelete}
            >
              <AiFillCloseCircle size={20} />
            </button>
          </Tooltip>
        </CardHeader>
      }
      <CardBody className="flex-row gap-4">
        <div>
          <SubtitleSegmentCounter
            label={"Start"}
            value={start}
            onChange={onStart}
          />
        </div>
        <Textarea value={text} onChange={onText} />
        <div>
          <SubtitleSegmentCounter label={"End"} value={end} onChange={onEnd} />
        </div>
      </CardBody>
    </Card>
  );
}
