import { useState } from "react";
import { API_BASE } from "../api";

export default function BookForm() {
  const [form, setForm] = useState({
    email: "",
    full_name: "",
    no_of_adults: 1,
    no_of_children: 0,
    arrival_year: 2025,
    arrival_month: 1,
    arrival_date: 1,
    avg_price_per_room: 100,
    market_segment_type: "Online",
    room_type_reserved: "Room_Type 1",
  });
  const [file, setFile] = useState(null);
  const [res, setRes] = useState(null);

  const onChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    const fd = new FormData();
    Object.entries(form).forEach(([k, v]) => fd.append(k, v));
    if (file) fd.append("id_image", file);
    const r = await fetch(`${API_BASE}/bookings/`, {
      method: "POST",
      body: fd,
    });
    setRes(await r.json());
  };

  return (
    <div className="p-6 max-w-xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold">احجز غرفتك</h1>
      <form onSubmit={submit} className="space-y-3">
        <input
          name="email"
          placeholder="Email"
          onChange={onChange}
          className="border p-2 w-full"
          required
        />
        <input
          name="full_name"
          placeholder="Full Name"
          onChange={onChange}
          className="border p-2 w-full"
        />
        <input
          type="number"
          name="no_of_adults"
          placeholder="Adults"
          onChange={onChange}
          className="border p-2 w-full"
          defaultValue={1}
        />
        <input
          type="number"
          name="no_of_children"
          placeholder="Children"
          onChange={onChange}
          className="border p-2 w-full"
          defaultValue={0}
        />
        <div className="grid grid-cols-3 gap-2">
          <input
            type="number"
            name="arrival_year"
            placeholder="Year"
            onChange={onChange}
            className="border p-2"
            defaultValue={2025}
          />
          <input
            type="number"
            name="arrival_month"
            placeholder="Month"
            onChange={onChange}
            className="border p-2"
            defaultValue={1}
          />
          <input
            type="number"
            name="arrival_date"
            placeholder="Day"
            onChange={onChange}
            className="border p-2"
            defaultValue={1}
          />
        </div>
        <input
          type="number"
          step="0.01"
          name="avg_price_per_room"
          placeholder="Avg Price"
          onChange={onChange}
          className="border p-2 w-full"
          defaultValue={100}
        />
        <input
          name="market_segment_type"
          placeholder="Segment"
          onChange={onChange}
          className="border p-2 w-full"
          defaultValue="Online"
        />
        <input
          name="room_type_reserved"
          placeholder="Room Type"
          onChange={onChange}
          className="border p-2 w-full"
          defaultValue="Room_Type 1"
        />
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setFile(e.target.files[0])}
          className="border p-2 w-full"
          required
        />
        <button className="bg-blue-600 text-white px-4 py-2 rounded">
          ارسال
        </button>
      </form>
      {res && (
        <div className="p-3 border rounded">
          <p>القبول: {res.accepted ? "✔️" : "❌"}</p>
          <p>Score: {res.score?.toFixed(2)}</p>
          <p>Offers: {JSON.stringify(res.offers)}</p>
          <p>Booking ID: {res.booking_id}</p>
        </div>
      )}
    </div>
  );
}
