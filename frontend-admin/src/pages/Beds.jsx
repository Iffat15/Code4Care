function Beds() {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Bed Management</h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white shadow rounded-xl p-6">
          <h3 className="text-gray-500">Total Beds</h3>
          <p className="text-2xl font-bold mt-2">100</p>
        </div>

        <div className="bg-white shadow rounded-xl p-6">
          <h3 className="text-gray-500">Available Beds</h3>
          <p className="text-2xl font-bold mt-2 text-green-600">34</p>
        </div>

        <div className="bg-white shadow rounded-xl p-6">
          <h3 className="text-gray-500">Occupied Beds</h3>
          <p className="text-2xl font-bold mt-2 text-red-600">66</p>
        </div>
      </div>
    </div>
  )
}

export default Beds