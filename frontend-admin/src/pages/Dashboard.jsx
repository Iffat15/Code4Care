// import StatCard from "../components/StatCard"

// function Dashboard() {
//   return (
//     <div>
//       <h2 className="text-2xl font-bold mb-6">Dashboard Overview</h2>

//       <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
//         <StatCard title="Active SOS Requests" value="12" />
//         <StatCard title="Available Beds" value="34" />
//         <StatCard title="On-Duty Staff" value="18" />
//         <StatCard title="Total Requests Today" value="56" />
//       </div>
//     </div>
//   )
// }

// export default Dashboard

import StatCard from "../components/StatCard"

function Dashboard() {
  return (
    <div className="space-y-10">

      {/* Page Title */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-primary">
          Overview
        </h1>

        <div className="bg-white px-4 py-2 rounded-xl shadow-sm border text-sm">
          Avg Response Time: 
          <span className="ml-2 font-semibold text-accent">
            4.2 min
          </span>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard title="Active SOS" value="12" />
        <StatCard title="Available Beds" value="34" />
        <StatCard title="On-Duty Staff" value="18" />
        <StatCard title="Today's Requests" value="56" />
      </div>

      {/* Bottom Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

        {/* Recent Activity */}
        <div className="bg-white rounded-2xl p-6 shadow-sm border">
          <h3 className="text-lg font-semibold mb-4">
            Recent Emergency Requests
          </h3>

          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <div>
                <p className="font-medium">Rahul Sharma</p>
                <p className="text-sm text-gray-500">Accident Case</p>
              </div>
              <span className="text-danger text-sm font-semibold">
                Pending
              </span>
            </div>

            <div className="flex justify-between items-center">
              <div>
                <p className="font-medium">Priya Verma</p>
                <p className="text-sm text-gray-500">Cardiac</p>
              </div>
              <span className="text-success text-sm font-semibold">
                Accepted
              </span>
            </div>
          </div>
        </div>

        {/* Performance Card */}
        <div className="bg-white rounded-2xl p-6 shadow-sm border">
          <h3 className="text-lg font-semibold mb-4">
            Hospital Capacity
          </h3>

          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-500 mb-1">
                Bed Occupancy
              </p>
              <div className="w-full bg-gray-200 h-3 rounded-full">
                <div className="bg-accent h-3 rounded-full w-2/3"></div>
              </div>
            </div>

            <div>
              <p className="text-sm text-gray-500 mb-1">
                ICU Usage
              </p>
              <div className="w-full bg-gray-200 h-3 rounded-full">
                <div className="bg-danger h-3 rounded-full w-3/4"></div>
              </div>
            </div>
          </div>
        </div>

      </div>

    </div>
  )
}

export default Dashboard