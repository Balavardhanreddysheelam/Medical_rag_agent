"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Upload, CheckCircle, AlertCircle } from "lucide-react";

export function UploadForm() {
    const [file, setFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

    const handleUpload = async () => {
        if (!file) return;

        setUploading(true);
        setMessage(null);

        const formData = new FormData();
        formData.append("file", file);

        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/upload`, {
                method: "POST",
                body: formData,
            });

            if (!res.ok) {
                const error = await res.json();
                throw new Error(error.detail || "Upload failed");
            }

            const data = await res.json();
            setMessage({ type: "success", text: `Uploaded ${data.filename}. Processed ${data.chunks_count} chunks.` });
            setFile(null);
        } catch (error: any) {
            setMessage({ type: "error", text: error.message });
        } finally {
            setUploading(false);
        }
    };

    return (
        <Card>
            <CardHeader>
                <CardTitle className="flex items-center gap-2">
                    <Upload className="w-5 h-5" />
                    Upload Medical Record
                </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                <Input
                    type="file"
                    accept=".pdf"
                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                    disabled={uploading}
                />
                {file && (
                    <div className="text-sm text-muted-foreground">
                        Selected: {file.name}
                    </div>
                )}
                <Button
                    onClick={handleUpload}
                    disabled={!file || uploading}
                    className="w-full"
                >
                    {uploading ? "Processing..." : "Upload & Ingest"}
                </Button>

                {message && (
                    <div className={`flex items-center gap-2 text-sm ${message.type === "success" ? "text-green-600" : "text-red-600"}`}>
                        {message.type === "success" ? <CheckCircle className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}
                        {message.text}
                    </div>
                )}
            </CardContent>
        </Card>
    );
}
