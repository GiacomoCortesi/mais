import { Card, CardBody, CardHeader } from "@heroui/card";
import { Divider } from "@heroui/divider";
import Link from "next/link";

import { title } from "@/components/primitives";

export default function Home() {
  return (
    <>
      <section className="h-full flex flex-col items-center justify-center gap-4 py-8 md:py-10">
        <div className="h-full inline-block max-w-lg text-center justify-center">
          <h1 className={title()}>Music AI Subtitles</h1>
          <p className="text-lg">AI-Powered subtitle generator</p>
          <div className="flex justify-center gap-4 mt-6">
            <Link href="/converter">
              <Card isPressable>
                <CardHeader>
                  <h4 className="font-bold text-large">MAIS Converter</h4>
                </CardHeader>
                <Divider />
                <CardBody>
                  <p>
                    Instantly create and edit subtitles from a music video or
                    audio
                  </p>
                </CardBody>
              </Card>
            </Link>
            <Link href="/transcription">
              <Card isPressable>
                <CardHeader>
                  <h4 className="font-bold text-large">Transcriptions</h4>
                </CardHeader>
                <Divider />
                <CardBody>
                  <p>Save and edit transcriptions</p>
                </CardBody>
              </Card>
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
