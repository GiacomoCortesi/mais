import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { createTranscription } from "@/actions/transcription";
import { ISubtitleJobConfig } from "@/types/job";
import JobInfoPopOver from "./job-info-popover";
import { Card, CardHeader, CardBody } from "@nextui-org/card";
import { Divider } from "@nextui-org/divider";

export interface Props {
  jobId: string;
  onStatusChange: (status: string) => void;
}

export default function JobStatus({ jobId, onStatusChange }: Props) {
  const router = useRouter();
  const [status, setStatus] = useState(null);
  const [jobInfo, setJobInfo] = useState<ISubtitleJobConfig>({
    video_file: "",
    config: {
      speaker_detection: false,
      subtitles_frequency: 0,
      language: "",
      model_size: "",
      hugging_face_token: "",
    },
  });
  let intervalId: NodeJS.Timeout;

  async function poll() {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/job/${jobId}`
    );
    const { status, config, data } = await response.json();

    setJobInfo(config);

    setStatus(status);
    onStatusChange(status);

    if (status === "finished") {
      clearInterval(intervalId);
      const { transcription_id: transcriptionId } = await createTranscription(
        data,
        jobId,
        config.video_file
      );

      router.push(`/transcription/${transcriptionId}`);
    }
    if (status === "failed") {
      clearInterval(intervalId);
    }
  }

  useEffect(() => {
    // call polling function to retrieve status immediately
    poll();
    // call polling function with setInterval to periodically poll for the status
    intervalId = setInterval(poll, 5000); // Poll every 5 seconds

    return () => clearInterval(intervalId); // Clean up on unmount
  }, []);

  return (
    <div>
      {jobId && (
        <Card className="m-2">
          <CardHeader className="flex gap-3">
            <JobInfoPopOver options={jobInfo.config} />
            Subtitles generation in progress
          </CardHeader>
          <Divider />
          <CardBody>
            <p>
              Generating subtitles for{" "}
              <span className="text-amber-300">{jobInfo.video_file}</span>
              <br /> Current status:{" "}
              <span
                className={
                  status == "failed" ? "text-red-300" : "text-green-300"
                }
              >
                {status}
              </span>
              <br />
              <span className="font-semibold">
                It may take few minutes so be patient, it is worth it!
              </span>
            </p>
          </CardBody>
        </Card>
      )}
    </div>
  );
}
