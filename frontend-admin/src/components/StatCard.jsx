function StatCard({ title, value }) {
  return (
    <div className="bg-white shadow rounded-xl p-6 w-full">
      <h3 className="text-gray-500 text-sm">{title}</h3>
      <p className="text-2xl font-bold mt-2">{value}</p>
    </div>
  )
}

export default StatCard