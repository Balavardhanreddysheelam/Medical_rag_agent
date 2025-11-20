import { UploadForm } from "@/components/upload-form";
import { ChatInterface } from "@/components/chat-interface";
import { UserButtonWrapper } from "@/components/user-button-wrapper";

export default function Home() {
  return (
    <div className="min-h-screen bg-background p-8">
      <header className="flex justify-between items-center mb-8 max-w-5xl mx-auto">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Medical RAG Agent</h1>
          <p className="text-muted-foreground">HIPAA-inspired query answering system</p>
        </div>
        <UserButtonWrapper />
      </header>

      <main className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-1">
          <UploadForm />

          <div className="mt-8 p-4 bg-muted/50 rounded-lg text-sm text-muted-foreground">
            <h3 className="font-semibold mb-2">Instructions</h3>
            <ol className="list-decimal list-inside space-y-1">
              <li>Upload a medical PDF (e.g., patient notes).</li>
              <li>System will redact PHI automatically.</li>
              <li>Ask questions in the chat panel.</li>
            </ol>
          </div>
        </div>

        <div className="md:col-span-2">
          <ChatInterface />
        </div>
      </main>
    </div>
  );
}
