export default function ScoreCard({ title, score }) {
  return (
    <div className="p-4 rounded-lg shadow bg-white">
      <h3 className="text-sm text-gray-500">{title}</h3>
      <p className="text-2xl font-bold">{score}점</p>
    </div>
  );
}
