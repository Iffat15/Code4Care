import { BrowserRouter, Routes, Route } from "react-router-dom"
import Dashboard from "./pages/Dashboard"
import Requests from "./pages/Requests"
import Beds from "./pages/Beds"
import Analytics from "./pages/Analytics"
import Sidebar from "./layout/Sidebar"
import Navbar from "./layout/Navbar"

function App() {
  return (
    <BrowserRouter>
    <Navbar/>
      <div className="flex">
        <Sidebar />
        <div className="flex-1 p-0 bg-gray-100 min-h-screen">
          
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/requests" element={<Requests />} />
            <Route path="/beds" element={<Beds />} />
            <Route path="/analytics" element={<Analytics />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  )
}

export default App