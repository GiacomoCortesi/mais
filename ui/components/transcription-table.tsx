"use client";
// need to use client component because of: https://github.com/nextui-org/nextui/issues/1342
import { useRouter } from "next/navigation";
import {
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
} from "@heroui/table";
import { Tooltip } from "@heroui/tooltip";
import { AiFillEdit, AiFillDelete } from "react-icons/ai";
import { Key, useCallback } from "react";

import { ITranscription } from "@/types/transcription";
import { deleteTranscription } from "@/actions/transcription";

export interface Props {
  transcriptions: ITranscription[];
}

export default function TranscriptionTable({ transcriptions }: Props) {
  const rows: {
    key: number;
    file: string;
    language: string;
    id: string;
  }[] = [];
  const router = useRouter();

  transcriptions.forEach((transcription, index) => {
    rows.push({
      key: index,
      file: transcription.filename,
      language: transcription.data.language,
      id: transcription.id,
    });
  });

  const columns = [
    {
      key: "file",
      label: "File",
    },
    {
      key: "language",
      label: "Language",
    },
    {
      key: "id",
      label: "ID",
    },
    {
      key: "actions",
      label: "Actions",
    },
  ];

  const renderCell = useCallback((row: any, columnKey: Key, index: number) => {
    const cellValue = row[columnKey.toString()];

    switch (columnKey) {
      case "actions":
        return (
          <div className="relative flex items-center gap-2">
            <Tooltip content="Edit transcription">
              <span className="text-lg text-default-400 cursor-pointer active:opacity-50">
                <AiFillEdit
                  onClick={() => {
                    router.push(`/transcription/${transcriptions[index]?.id}`);
                  }}
                />
              </span>
            </Tooltip>
            <Tooltip color="danger" content="Delete transcription">
              <span className="text-lg text-danger cursor-pointer active:opacity-50">
                <AiFillDelete
                  onClick={deleteTranscription.bind(
                    null,
                    transcriptions[index]?.id,
                  )}
                />
              </span>
            </Tooltip>
          </div>
        );
      default:
        return cellValue;
    }
  }, []);

  return (
    <>
      {transcriptions.length ? (
        <Table removeWrapper aria-label="Example static collection table">
          <TableHeader columns={columns}>
            {(column) => (
              <TableColumn key={column.key}>{column.label}</TableColumn>
            )}
          </TableHeader>
          <TableBody items={rows}>
            {(item) => (
              <TableRow key={item.key}>
                {(columnKey) => (
                  <TableCell>{renderCell(item, columnKey, item.key)}</TableCell>
                )}
              </TableRow>
            )}
          </TableBody>
        </Table>
      ) : (
        <p>No trascription available yet</p>
      )}
    </>
  );
}
