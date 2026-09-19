import { useState } from "react";

export default function SearchBar({ onSearch }) {
  const [address, setAddress] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (address.trim()) onSearch(address.trim());
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="text"
        value={address}
        onChange={(e) => setAddress(e.target.value)}
        placeholder="예: 부산광역시 해운대구 우동"
        className="flex-1 border rounded-lg px-4 py-2"
      />
      <button type="submit" className="bg-blue-600 text-white rounded-lg px-4 py-2">
        검색
      </button>
    </form>
  );
}
