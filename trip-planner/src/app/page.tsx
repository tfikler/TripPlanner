import TripForm from "@/components/TripForm";

export default function Home() {
  return (
  <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundColor: '#f0f2f5' }}>
      <div>
        <h1 style={{ textAlign: 'center' }}>Trip Planner</h1>
        <TripForm />
      </div>
    </div>
  );
}
