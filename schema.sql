-- Optional persistence schema. Apply in the Supabase SQL editor after creating a project.
create extension if not exists pgcrypto;

create table if not exists public.trips (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  destination text not null,
  start_date date not null,
  duration_days integer not null check (duration_days between 1 and 21),
  preferences jsonb not null default '{}'::jsonb,
  itinerary jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

alter table public.trips enable row level security;
create policy "Users can read their own trips" on public.trips for select using (auth.uid() = user_id);
create policy "Users can create their own trips" on public.trips for insert with check (auth.uid() = user_id);
create policy "Users can update their own trips" on public.trips for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "Users can delete their own trips" on public.trips for delete using (auth.uid() = user_id);
