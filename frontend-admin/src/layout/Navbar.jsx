function Navbar() {
  return (
    <div className="bg-blue-700 h-16 flex items-center justify-between px-8 border-b border-gray-200">
      
      <h2 className="text-lg font-semibold text-gray-700">
        Admin Dashboard
      </h2>

      <div className="flex items-center gap-4">
        <div className="text-sm text-gray-500">
          Welcome back 👋
        </div>

        <div className="w-10 h-10 rounded-full bg-accent text-white flex items-center justify-center font-bold">
          A
        </div>
      </div>

    </div>
  )
}

export default Navbar