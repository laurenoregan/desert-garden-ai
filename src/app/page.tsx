import { supabase } from "@/lib/supabase";

export default async function Home() {
  const { data: garden } = await supabase
    .from("gardens")
    .select("*, beds(*, plantings(*, crops(*)))")
    .single();

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <h1 className="text-3xl font-semibold tracking-tight">Desert Garden AI</h1>
      {garden ? (
        <div className="mt-6 text-center">
          <p className="text-zinc-500">{garden.location_name}</p>
          <ul className="mt-4 space-y-1 text-sm text-zinc-400">
            {garden.beds?.map((bed: { id: number; name: string }) => (
              <li key={bed.id}>{bed.name}</li>
            ))}
          </ul>
        </div>
      ) : (
        <p className="mt-4 text-zinc-500">Your daily brief is coming soon.</p>
      )}
    </main>
  );
}
