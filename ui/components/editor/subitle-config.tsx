import {Slider} from "@heroui/slider";

import { subtitle } from "@/components/primitives";

import { TwitterPicker } from 'react-color'
import { ISubtitleConfig } from "@/types/video";
import { useTheme } from 'next-themes';

import {Select, SelectItem} from "@heroui/select";

interface Props {
    subtitleConfig: ISubtitleConfig;
    setSubtitleConfig: (value: any) => void;
}

const fonts = [
  {
    name: "Times New Roman",
    description: "A classic serif font, suitable for formal and professional subtitles.",
    cssValue: '"Times New Roman", Times, serif',
  },
  {
    name: "Georgia",
    description: "A serif font that is modern and elegant, designed for better readability on screens.",
    cssValue: '"Georgia", serif',
  },
  {
    name: "Merriweather",
    description: "A serif font optimized for readability on digital screens.",
    cssValue: '"Merriweather", serif',
  },
  {
    name: "Playfair Display",
    description: "A sophisticated serif font with high contrast, ideal for dramatic subtitles.",
    cssValue: '"Playfair Display", serif',
  },
  {
    name: "Garamond",
    description: "A timeless serif font with a clean and classic feel, suitable for formal subtitles.",
    cssValue: '"Garamond", serif',
  },
  {
    name: "Arial",
    description: "A simple, clean, and widely used sans-serif font.",
    cssValue: '"Arial", sans-serif',
  },
  {
    name: "Helvetica",
    description: "A modern, neutral, and professional sans-serif font, often used for clean subtitles.",
    cssValue: '"Helvetica", Arial, sans-serif',
  },
  {
    name: "Roboto",
    description: "A geometric and modern sans-serif font, perfect for subtitles in digital videos.",
    cssValue: '"Roboto", sans-serif',
  },
  {
    name: "Open Sans",
    description: "A clean and highly readable sans-serif font often used for subtitles.",
    cssValue: '"Open Sans", sans-serif',
  },
  {
    name: "Lato",
    description: "A sleek sans-serif font with a friendly and elegant feel.",
    cssValue: '"Lato", sans-serif',
  },
  {
    name: "Poppins",
    description: "A bold and geometric sans-serif font, great for subtitles in modern videos.",
    cssValue: '"Poppins", sans-serif',
  },
  {
    name: "Montserrat",
    description: "A trendy, minimalist sans-serif font with a sleek and modern look.",
    cssValue: '"Montserrat", sans-serif',
  },
  {
    name: "Nunito",
    description: "A balanced and rounded sans-serif font that looks soft and clean.",
    cssValue: '"Nunito", sans-serif',
  },
  {
    name: "Courier New",
    description: "A classic monospace font for a typewriter-like feel.",
    cssValue: '"Courier New", Courier, monospace',
  },
  {
    name: "Source Code Pro",
    description: "A modern monospace font, great for a tech-inspired look.",
    cssValue: '"Source Code Pro", monospace',
  },
  {
    name: "Fira Code",
    description: "A stylish and developer-friendly monospace font with ligatures.",
    cssValue: '"Fira Code", monospace',
  },
  {
    name: "Oswald",
    description: "A condensed sans-serif font that is modern and great for impactful subtitles.",
    cssValue: '"Oswald", sans-serif',
  },
  {
    name: "Raleway",
    description: "A stylish and elegant sans-serif font with a touch of class.",
    cssValue: '"Raleway", sans-serif',
  },
  {
    name: "Bebas Neue",
    description: "A bold and condensed sans-serif font, great for attention-grabbing subtitles.",
    cssValue: '"Bebas Neue", sans-serif',
  },
  {
    name: "Caveat",
    description: "A handwritten-style font with a casual and personal touch.",
    cssValue: '"Caveat", cursive',
  },
  {
    name: "Dancing Script",
    description: "A playful and elegant script font for a handwritten feel.",
    cssValue: '"Dancing Script", cursive',
  },
];

export const SubtitleConfig = ({ subtitleConfig, setSubtitleConfig }: Props) => {
  const { theme, setTheme } = useTheme();

  const handleChangeComplete = (color: any) => {
    setSubtitleConfig((prev: any) => ({ ...prev, color: color.hex }));
  };
  const handleFontSizeChange = (value: any) => {
    console.log(value[0])
    setSubtitleConfig((prev: any) => ({ ...prev, size: value[0] }));
  };
  const handlePositionChange = (value: any) => {
    setSubtitleConfig((prev: any) => ({ ...prev, position: value[0] }));
  }
  const handleFontChange = (e: any) => {
    const cssFont = fonts.find(font => font.name === e.target.value)?.cssValue;
    setSubtitleConfig((prev: any) => ({ ...prev, font: cssFont }));
  }

  const pickerStyles = {
    default: {
      card: {
        background: theme === 'dark' ? '#1F2937' : '#FFFFFF', // Tailwind's gray-800 and white
      },
    },
  };

    return (
        <div className="flex flex-col items-center">
            <h1 className={subtitle()}>Subtitle Config</h1>
            <Select value={subtitleConfig.font} onChange={handleFontChange} className="max-w-xs" label="Subtitles Font" placeholder="Select subtitle font">
              {fonts.map((font) => (
              <SelectItem key={font.name}>{font.name}</SelectItem>
            ))}
      </Select>
            <div>
              <p>Font Size</p>
              <Slider
                key={"secondary"}
                aria-label="Font Size"
                className="w-64"
                color={"secondary"}
                value={subtitleConfig.size}
                maxValue={100}
                minValue={1}
                step={1}
                onChange={handleFontSizeChange}
              />
            </div>
            <div>
              <p>Font Color</p>
              <TwitterPicker
                triangle="hide"
                styles={pickerStyles}
                className="bg-gray-800"
                color={ subtitleConfig?.color }
                onChangeComplete={ handleChangeComplete } />
            </div>
            <div>
              <p>Font Position</p>
              <Slider
                key={"secondary"}
                aria-label="Font Position"
                className="w-64"
                color={"secondary"}
                value={subtitleConfig?.position}
                maxValue={100}
                minValue={0}
                step={1}
                onChange={handlePositionChange}
              />
            </div>
        </div>
    );
}