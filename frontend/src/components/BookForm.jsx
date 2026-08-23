import { useState } from "react";
import { API_BASE } from "../api";

export default function BookForm() {
  const [form, setForm] = useState({
    email: "",
    full_name: "",
    no_of_adults: 1,
    no_of_children: 0,
    no_of_weekend_nights: 0,
    no_of_week_nights: 0,
    required_car_parking_space: 0,
    lead_time: 0,
    arrival_year: 2025,
    arrival_month: 1,
    arrival_date: 1,
    repeated_guest: 0,
    no_of_previous_cancellations: 0,
    no_of_previous_bookings_not_canceled: 0,
    avg_price_per_room: 100,
    no_of_special_requests: 0,
    type_of_meal_plan: "Meal Plan 1",
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
        <input
          type="number"
          name="no_of_weekend_nights"
          placeholder="Weekend nights"
          onChange={onChange}
          className="border p-2 w-full"
          defaultValue={0}
        />
        <input
          type="number"
          name="no_of_week_nights"
          placeholder="Week nights"
          onChange={onChange}
          className="border p-2 w-full"
          defaultValue={0}
        />
        <input
          type="number"
          name="required_car_parking_space"
          placeholder="Parking spaces"
          onChange={onChange}
          className="border p-2 w-full"
          defaultValue={0}
        />
        <input
          type="number"
          name="lead_time"
          placeholder="Lead time (days)"
          onChange={onChange}
          className="border p-2 w-full"
          defaultValue={0}
          required
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
          name="repeated_guest"
          placeholder="Repeated guest (0 or 1)"
          onChange={onChange}
          className="border p-2 w-full"
          defaultValue={0}
        />
        <input
          type="number"
          name="no_of_previous_cancellations"
          placeholder="Previous cancellations"
          onChange={onChange}
          className="border p-2 w-full"
          defaultValue={0}
        />
        <input
          type="number"
          name="no_of_previous_bookings_not_canceled"
          placeholder="Previous non-canceled bookings"
          onChange={onChange}
          className="border p-2 w-full"
          defaultValue={0}
        />
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
          type="number"
          name="no_of_special_requests"
          placeholder="Special requests"
          onChange={onChange}
          className="border p-2 w-full"
          defaultValue={0}
        />
        <select
          name="type_of_meal_plan"
          onChange={onChange}
          className="border p-2 w-full"
          defaultValue="Meal Plan 1"
        >
          <option>Meal Plan 1</option>
          <option>Meal Plan 2</option>
          <option>Meal Plan 3</option>
          <option>Not Selected</option>
        </select>
        <select
          name="market_segment_type"
          onChange={onChange}
          className="border p-2 w-full"
          defaultValue="Online"
        >
          <option>Aviation</option>
          <option>Complementary</option>
          <option>Corporate</option>
          <option>Offline</option>
          <option>Online</option>
        </select>
        <select
          name="room_type_reserved"
          onChange={onChange}
          className="border p-2 w-full"
          defaultValue="Room_Type 1"
        >
          <option>Room_Type 1</option>
          <option>Room_Type 2</option>
          <option>Room_Type 3</option>
          <option>Room_Type 4</option>
          <option>Room_Type 5</option>
          <option>Room_Type 6</option>
          <option>Room_Type 7</option>
        </select>
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
          <p>Database ID: {res.database_id}</p>
        </div>
      )}
    </div>
  );
}
