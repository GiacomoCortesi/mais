"use client";
import { Image } from "@nextui-org/image";
import { FaImage } from "react-icons/fa";
import { useState, useEffect, useRef } from "react";
import { Button } from "@nextui-org/button";

export interface Props {
  alt: string;
  src: string;
  onSelectVideo: any;
}

export default function PreviewImage({ alt, src, onSelectVideo }: Props) {
  const [imageLoaded, setImageLoaded] = useState(false);
  const cardRefs = useRef<HTMLDivElement[] | null>([]);
  const handleClickOutside = (event: Event) => {
    if (
      cardRefs?.current?.every(
        (ref) => ref && !ref.contains(event.target as Node),
      )
    ) {
      onSelectVideo("");
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    const checkImage = async () => {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${src}`, {
        method: "HEAD",
      });

      if (response.ok) {
        setImageLoaded(true);
      }
    };

    checkImage();

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [src]);

  return (
    <div className="flex justify-center h-28 items-center w-full">
      {imageLoaded ? (
        <Image
          isZoomed
          alt={alt}
          className="object-fit w-full h-28"
          src={`${process.env.NEXT_PUBLIC_API_URL}${src}`}
          onClick={() => {
            onSelectVideo(alt);
          }}
          onError={() => setImageLoaded(false)}
        />
      ) : (
        <Button
          disableAnimation
          disableRipple
          isIconOnly
          className="flex justify-center h-28 items-center w-full"
          variant="light"
          onClick={() => onSelectVideo(alt)}
        >
          <FaImage className="w-full h-100%" size={50} />
        </Button>
      )}
    </div>
  );
}
