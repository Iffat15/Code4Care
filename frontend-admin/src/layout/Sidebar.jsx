import { Link } from "react-router-dom"
import { LayoutDashboard, Ambulance, Bed, BarChart } from "lucide-react"

function Sidebar() {
  return (
    // <div className="w-64  text-black min-h-screen p-6 shadow-lg">
    <div className="w-64 bg-white min-h-screen p-6 border-r border-gray-200 shadow-[4px_0_12px_rgba(0,0,0,0.06)]">
      {/* <h1 className="text-xl font-bold mb-8">Code4Care Admin</h1> */}

      <nav className="flex flex-col gap-4">
        <Link to="/" className="flex gap-2 items-center hover:text-gray-300">
          <LayoutDashboard size={18} /> Dashboard
        </Link>
        <Link to="/requests" className="flex gap-2 items-center hover:text-gray-300">
          <Ambulance size={18} /> Requests
        </Link>
        <Link to="/beds" className="flex gap-2 items-center hover:text-gray-300">
          <Bed size={18} /> Beds
        </Link>
        <Link to="/analytics" className="flex gap-2 items-center hover:text-gray-300">
          <BarChart size={18} /> Analytics
        </Link>
      </nav>
    </div>
  )
}

export default Sidebar