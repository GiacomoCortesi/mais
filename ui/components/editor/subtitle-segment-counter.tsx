"use client";

import React, { ChangeEventHandler } from "react";
import { Input } from "@heroui/input";

export interface Props {
  label: string;
  value: number;
  onChange: ChangeEventHandler;
}

export default function SubtitleSegmentCounter({
  label,
  value,
  onChange,
}: Props) {
  return (
    <Input
      endContent={
        <div className="pointer-events-none flex items-center">
          <span className="text-default-400 text-small">s</span>
        </div>
      }
      label={label}
      labelPlacement="outside"
      type="number"
      value={value.toString()}
      onChange={onChange}
    />
  );
}
