function Requests() {
  const requests = [
    { id: 1, name: "Rahul Sharma", type: "Accident", status: "Pending" },
    { id: 2, name: "Priya Verma", type: "Cardiac", status: "Accepted" },
    { id: 3, name: "Amit Patel", type: "Burn Injury", status: "Pending" },
  ]

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Emergency Requests</h2>

      <div className="bg-white shadow rounded-xl p-6">
        <table className="w-full text-left">
          <thead>
            <tr className="border-b">
              <th className="py-3">Patient</th>
              <th>Type</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {requests.map((req) => (
              <tr key={req.id} className="border-b">
                <td className="py-3">{req.name}</td>
                <td>{req.type}</td>
                <td>
                  <span
                    className={`px-3 py-1 rounded-full text-sm ${
                      req.status === "Pending"
                        ? "bg-red-100 text-red-600"
                        : "bg-green-100 text-green-600"
                    }`}
                  >
                    {req.status}
                  </span>
                </td>
                <td className="flex gap-2 py-3">
                  <button className="bg-green-500 text-white px-3 py-1 rounded">
                    Accept
                  </button>
                  <button className="bg-red-500 text-white px-3 py-1 rounded">
                    Reject
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Requests