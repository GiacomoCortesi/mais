import {
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownSection,
  DropdownItem,
} from "@heroui/dropdown";
import { Button } from "@heroui/button";
import { Slider } from "@heroui/slider";
import { Select, SelectItem } from "@heroui/select";
import { Switch } from "@heroui/switch";
import React from "react";

import { ISubtitleJobOptions } from "@/types/job";

import { CogFilledIcon } from "../icons";

export interface Props {
  isDisabled: boolean;
  options: ISubtitleJobOptions;
  onOptionUpdate: (key: string, value: any) => void;
}

export default function SettingsDropdown({
  isDisabled,
  options,
  onOptionUpdate,
}: Props) {
  const modelSizes = [
    { key: "tiny", label: "Tiny" },
    { key: "small", label: "Small" },
    { key: "medium", label: "Medium" },
    { key: "large", label: "Large" },
  ];

  const languages = [
    { key: "en", label: "English" },
    { key: "it", label: "Italian" },
    { key: "es", label: "Spanish" },
    { key: "pt", label: "Portuguese" },
  ];

  return (
    <>
      <Dropdown backdrop="blur" closeOnSelect={false}>
        <DropdownTrigger>
          <Button isIconOnly color="default" isDisabled={isDisabled}>
            <CogFilledIcon className="text-default-500" />
          </Button>
        </DropdownTrigger>
        <DropdownMenu aria-label="Select settings">
          <DropdownSection showDivider title="Model language">
            <DropdownItem key="model_size" textValue="model_size">
              <Select
                label="Select model size"
                name="model_size"
                selectedKeys={new Set([options.model_size])}
                value={options.model_size}
                onChange={(e) => onOptionUpdate("model_size", e.target.value)}
              >
                {modelSizes.map((modelSize) => (
                  <SelectItem key={modelSize.key} textValue={modelSize.label}>
                    {modelSize.label}
                  </SelectItem>
                ))}
              </Select>
            </DropdownItem>
            <DropdownItem key="language" textValue="language">
              <Select
                label="Select language"
                name="language"
                selectedKeys={new Set([options.language])}
                value={options.language}
                onChange={(e) => onOptionUpdate("language", e.target.value)}
              >
                {languages.map((lang) => (
                  <SelectItem key={lang.key} textValue={lang.label}>
                    {lang.label}
                  </SelectItem>
                ))}
              </Select>
            </DropdownItem>
          </DropdownSection>
          <DropdownSection showDivider title="Subtitles frequency">
            <DropdownItem key="subtitles_frequency" textValue="settings">
              <Slider
                className="max-w-md"
                label={`Subtitles frequency (s):  `}
                maxValue={50}
                minValue={0}
                name="subtitles_frequency"
                step={1}
                value={options.subtitles_frequency}
                onChange={(e) => onOptionUpdate("subtitles_frequency", e)}
              />
            </DropdownItem>
          </DropdownSection>
          <DropdownSection title="Speaker detection">
            <DropdownItem key="speaker_detection" textValue="speaker_detection">
              <Switch
                isSelected={options.speaker_detection}
                onValueChange={(e) => onOptionUpdate("speaker_detection", e)}
              >
                Speaker detection
              </Switch>
            </DropdownItem>
          </DropdownSection>
        </DropdownMenu>
      </Dropdown>
    </>
  );
}
