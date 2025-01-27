export type SiteConfig = typeof siteConfig;

export const siteConfig = {
  name: "MAIS",
  description: "Convert music videos into subtitles through the power of AI",
  navItems: [
    {
      label: "Converter",
      href: "/converter",
    },
    {
      label: "Transcriptions",
      href: "/transcription",
    },
  ],
  navMenuItems: [
    {
      label: "Converter",
      href: "/converter",
    },
    {
      label: "Transcriptions",
      href: "/transcription",
    },
  ],
  links: {
    github: "https://github.com/GiacomoCortesi/music-ai-sub",
    api: `${process.env.API_URL}/docs`,
  },
};
